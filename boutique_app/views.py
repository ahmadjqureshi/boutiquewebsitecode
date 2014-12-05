from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from boutique_app.models import Users
from boutique_app.models import Products
from boutique_app.models import ProductImages
from django.core.context_processors import csrf
import datetime
from django.conf import settings
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

# Create your views here.
def hello(request):
    now = datetime.datetime.now()
    
    pname = 'Ahmad Qureshi'

    all_users = Users.objects.all()
    
    item_list = []
    
    for user in all_users:
        disp = user.LoginName + ' : ' + user.Password
        item_list.append(disp)
#    item_list.append('XYZ')
    
    warranty = True
    
    company = 'Hus hemma'
	
    contextDictionary = {}
    contextDictionary['person_name'] = pname
    contextDictionary['company'] = company
    contextDictionary['ship_date'] = now
    contextDictionary['item_list'] = item_list
    contextDictionary['ordered_warranty'] = warranty
    
    t = get_template('first_template.html')

    html = t.render( Context( contextDictionary ))

    return HttpResponse(html)

def index(request):
    t = get_template('index.html')
    contextDictionary = {}
    
    html = t.render( Context( contextDictionary ))

    return HttpResponse(html)

def add_product_step1_form(request):
    t = get_template('add_product_step1.html')
    
    authenticated = False
    
    try:
        if request.user is not None:
            authenticated = request.user.is_authenticated()
    except:
        authenticated = False
    
    if authenticated == False:
        return HttpResponseRedirect("/index/")

    contextDictionary = {}
    contextDictionary.update(csrf(request))
    if authenticated == True:
        contextDictionary["UserName"] = request.user.get_username()
    
    html = t.render( Context( contextDictionary ) )

    return HttpResponse( html )

def ajaxtest(request):
    
    maxRec = int(0)

    numberOfProducts = Products.objects.count()

    if numberOfProducts > 0:
        latestObject = Products.objects.latest('ProductID')
        maxRec = int(latestObject.ProductID)
    
    maxRec = maxRec + 1
    
    if request.method == 'POST':
        pHeading = request.POST["heading"]
        pDescription = request.POST["description"]
        pPrice = request.POST["price"]
    
        newProduct = Products( ProductID=maxRec, Heading = pHeading, Description = pDescription, Price = pPrice)
        newProduct.save()

        request.session["Product"] = newProduct.ProductID

        message = request.POST["heading"] + "<br>" + request.POST["description"] + "<br>" + request.POST["price"]
    
        return HttpResponse(message)
    return HttpResponse('')

def imageupload(request):
    pathToImages = settings.STATICFILES_DIRS[4][1]
    extension = ".jpeg"
    prefixFile = "Image"
    prefixThumbNail = "ThumbNail"

    maxCount = 0

    if ProductImages.objects.count() > 0:
        latestObject1 = ProductImages.objects.latest('ImageID')
        maxCount = int(latestObject1.ImageID)

    productID = int( request.session["Product"] )

    message = "No Of file: " + request.FILES['file1'].name
    newFile = request.FILES['file1']

    imageName = prefixFile + str(maxCount) + extension
    thumbNailName = prefixThumbNail + str(maxCount) + extension

    imagePath = pathToImages  + imageName
    thumbnailPath = pathToImages  + thumbNailName
    
    newWrite = open( imagePath, 'wb+')
    for chunk in newFile.chunks():
        newWrite.write(chunk)
    
    newWrite.close()
    
    size = 80, 80
    
    out_file = open( thumbnailPath, 'wb' )
    im = Image.open(imagePath)
    im.thumbnail(size)
    im.save( out_file, "JPEG")
    out_file.flush()
    out_file.close()
    
    pProduct = Products.objects.get(ProductID=productID)
    
    maxCount = maxCount + 1
    
    pImage = ProductImages( ProductFK = pProduct, ImageID = maxCount, ImageName = imageName, ThumbNail = thumbNailName)
    pImage.save()
    
    t = get_template('uploaded_image.html')
    contextDictionary = {}
    contextDictionary["RowID"] = str(maxCount)
    contextDictionary["ThumbNailName"] = thumbNailName
    
    html = t.render( Context( contextDictionary ))
    
    return HttpResponse(html)

def deleteimage(request):
    imageID = request.POST["ImageID"]

    instanceProductImages = ProductImages.objects.get(ImageID=int(imageID))
    instanceProductImages.delete()

    return HttpResponse("")

class ProductItem:
    productHeading = ""
    productImage = ""
    productPrice = ""
    productID = int(0)
    def __init__( self, id, heading, image, price):
        self.productHeading = heading
        self.productImage = image
        self.productPrice = price
        self.productID = id
    

def viewproducts(request):
    numOfRowsPerPage = 10
    isFirstPage = False
    isLastPage  = False
    nextPage = int(0)
    lastPage = int(0)
    currentPage = 0
    pListItems = []
    query = ""
    
    if request.method == 'POST':
        query = str( request.POST["query"] )
        request.session["query"] = query
        currentPage = 1
        
    else:
        try:
            currentPage = int(request.GET.get('page'))
        except:
            currentPage = 1

    try:
        query = str(request.session["query"])
    except:
        query = ""
    
    pProducts = Products.objects.filter(Description__icontains=query)

    endRow = currentPage * numOfRowsPerPage
    startRow = endRow - numOfRowsPerPage +1
    
    if endRow > pProducts.count():
        endRow = pProducts.count()

    while startRow <= endRow:
        pImage = ProductImages.objects.filter(ProductFK = pProducts[ startRow - 1])
        imageName = ""
        if pImage.count() > 0:
            imageName = pImage[0].ThumbNail

        pPrice = pProducts[ startRow - 1].Price

        pItem = ProductItem( id = pProducts[ startRow - 1].ProductID, heading = pProducts[ startRow - 1].Heading,image = imageName, price = pPrice )
        pListItems.append( pItem )
        
        startRow = startRow + 1
        
    if endRow >= pProducts.count():
        isLastPage = True
    
    if currentPage == 1:
        isFirstPage = True

    t = get_template('viewproducts.html')
    
    contextDictionary = {}
    contextDictionary.update(csrf(request))
    contextDictionary["item_list"] = pListItems

    if isFirstPage:
        contextDictionary["previousPage"] =  0
    else:
        contextDictionary["previousPage"] =  1

    if isLastPage:
        contextDictionary["nextPage"] =  0
    else:
        contextDictionary["nextPage"] =  1
    
    contextDictionary["previousPageNum"] = currentPage - 1
    contextDictionary["nextPageNum"] = currentPage + 1
    request.session["currentPage"] = currentPage
    contextDictionary["QueryString"] = query
    
    html = t.render( Context( contextDictionary ) )
    
    return HttpResponse( html )

class ImageItem:
    imageName = ""
    imageID = ""
    linkedID = ""
    
    def __init__( self, imgID, name, lID):
        self.imageID = imgID
        self.imageName = name
        self.linkedID = lID

def productdetail(request):
    productID = request.GET.get('id')
    product = Products.objects.get( ProductID = productID)
    
    productHeading = product.Heading
    productDescription = product.Description
    productPrice = product.Price
    
    productImages = []
    productThumbNails = []
    productImageIDs = []
    thumbNailIDs = []
    i = 0
    
    pImages = ProductImages.objects.filter( ProductFK = product )
    
    for rec in pImages:
        imageID = "Image" + str(i)
        thumbNailID = "ThumbNail" + str(i)
        imgItem = ImageItem( imgID = imageID, name = rec.ImageName, lID = "")
        productImages.append( imgItem )
        
        thumbNailItem = ImageItem( imgID = thumbNailID, name = rec.ThumbNail, lID = imageID)
        productThumbNails.append( thumbNailItem )
        i = i + 1
    
    
    t = get_template('productdetail.html')
    
    contextDictionary = {}
    contextDictionary["imageList"] = productImages
    contextDictionary["thumbNailList"] = productThumbNails
    contextDictionary["pageNumber"] = request.session["currentPage"]
    contextDictionary["Heading"] = productHeading
    contextDictionary["Price"] = productPrice
    contextDictionary["Details"] = productDescription

    html = t.render( Context( contextDictionary ) )
    
    return HttpResponse( html )

def loginform(request):
    authenticated = False
    
    try:
        if request.user is not None:
            authenticated = request.user.is_authenticated()
    except:
        authenticated = False

    if authenticated == True:
        return HttpResponseRedirect("/mainpage/")


    t = get_template('login.html')
    
    contextDictionary = {}
    contextDictionary.update(csrf(request))
    contextDictionary["LoginError"] = ""
    
    html = t.render( Context( contextDictionary ) )
    
    return HttpResponse( html )

def loginprocess(request):
    uname = request.POST["uname"]
    upwd = request.POST["upwd"]
    
    user = authenticate(username=uname, password=upwd)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/mainpage/")
        else:
            # Return a 'disabled account' error message
            t = get_template('login.html')
            
            contextDictionary = {}
            contextDictionary.update(csrf(request))
            contextDictionary["LoginError"] = "User disabled contact admin."
            
            html = t.render( Context( contextDictionary ) )
    
            return HttpResponse( html )
    else:
        # Return an 'invalid login' error message.
        t = get_template('login.html')
            
        contextDictionary = {}
        contextDictionary.update(csrf(request))
        contextDictionary["LoginError"] = "Invalid User."
        
        html = t.render( Context( contextDictionary ) )
        
        return HttpResponse( html )
    
    return HttpResponse( html )

def mainpage(request):
    authenticated = False
    
    try:
        if request.user is not None:
            authenticated = request.user.is_authenticated()
    except:
        authenticated = False

    if authenticated == True:
        t = get_template('mainpage.html')
        
        contextDictionary = {}
        contextDictionary["UserName"] = request.user.get_username()

        html = t.render( Context( contextDictionary ) )
        
        return HttpResponse( html )

    return HttpResponseRedirect("/index/")

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect("/index/")

def contact(request):
     t = get_template('contact.html')
        
     contextDictionary = {}
     
     html = t.render( Context( contextDictionary ) )
     
     return HttpResponse( html )
