from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from realtime.actualbrain import actualData, plot2y, actual_Data, plot1y, plot4y, plot3y
from realtime.models import tower
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import numpy as np
from realtime.serializers import tower_serializer


# Create your views here.

def trial(request):
    return HttpResponse(len(plot1y))


@api_view(["GET"])
def towers_detail(request):
    name = request.GET.get('name')

    if(name == 'towerone'):
        tower_data = tower.objects.values()[:13]
    elif(name == 'towertwo'):
        tower_data = tower.objects.values()[13:25]
    elif(name == 'towerthree'):
        tower_data = tower.objects.values()[25:37]
    elif(name == 'towerfour'):
        tower_data = tower.objects.values()[37:49]
    elif(name == 'towerfive'):
        tower_data = tower.objects.values()[49:61]


    pred = []
    act = [] 
    diff = [] 
    for i in tower_data:
        serialize = tower_serializer(i)
        pred.append(tofloat((serialize.data['predicted_Usage'][1:-1]).split(',')))
        act.append(tofloat((serialize.data['actual_Usage'][1:-1]).split(',')))
        diff.append(tofloat((serialize.data['difference'][1:-1]).split(',')))
    pred = listwala(pred)
    act = listwala(act)
    diff = listwala(diff)

    return JsonResponse({
        "predicted_Usage":pred,
        "actual_Usage":act,
        "difference":diff


    })

def listwala(l):
    flat_list = []
    for sublist in l:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def tofloat(x):
    test_list = []
    for i in range(1, len(x)): 
        # if(x[i]==',' or x[i]=='.'):
        #     continue
        test_list.append(float(x[i]))
    return test_list

def sendtoDb(request):
    temp = toListJson(plot1y)+toListJson(plot2y) + toListJson(plot3y) + toListJson(plot4y)
    actual = toListJson(actualData)
    difference = getDifference()
    actual = actual[48:]
    for i in actual:
        p = tower(actual_Usage=i)
    # for i in range(48):
    #     t1 = temp[i]
    #     t2 = actual[i]
    #     t3 = difference[i]

    #     p = tower(predicted_Usage=t1,actual_Usage=t2,difference=t3)
       

        p.save()
    return HttpResponse("it worked")


    

@api_view(["GET"])
def sports_events_get_name_poster(request):
    sports_data = []
    for i in tower.objects.values():
        sports_data.append(i)
    return JsonResponse({'data': sports_data})

def getDifference():
    temp = toListJson(plot1y)+toListJson(plot2y) + toListJson(plot3y) + toListJson(plot4y)
    temp2 = toListJson(actualData)
    answer = []
    for i in range(48):
        answer.append(np.ndarray.tolist(np.array(temp[i])-np.array(temp2[i])))
    return answer
    # return JsonResponse({
    #     "Data":answer
    # })
    
    

def kuchbhi(request):
    data = {
        "data":toListJson(actualData),
    }
    return JsonResponse(data)

def toListJson(datacell1):
    c = 0
    list1 = [] 
    str = []
    for i in datacell1:        
        str.append(i)      
        c +=1
        if c == 38:
            list1.append(str)
            c=0
            str=[]   
    print(len(list1))       
    return list1
