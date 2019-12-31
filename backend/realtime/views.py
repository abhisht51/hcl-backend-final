from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json 
from realtime.actualbrain import actualData,plot2y,actual_Data,plot1y,plot4y,plot3y
from realtime.models import tower
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import numpy as np


# Create your views here.

def trial(request):
    return HttpResponse(len(plot1y))


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

        # p = tower(predicted_Usage=t1,actual_Usage=t2,difference=t3)
        # p = tower(actual_Usage = actual[i])
        # p = tower(difference = difference[i])

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