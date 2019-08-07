from Tesla.response import render,HttpResponse
def index(request):
    #HttpResponse(request,"Hello")
    return render(request,'\A Neural Network Playground.html')