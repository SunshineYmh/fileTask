# from django.http import HttpResponse
# # from django.template import loader
# from django.shortcuts import get_object_or_404, render

# def index(request):
#     # latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("PDFesc/index.html")
#     # context = {
#     #     "latest_question_list": latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "PDFesc/index.html", context)

# def libjsRoute(request, file_name):
#     return render(request, "PDFesc/lib/" + file_name, locals())

# def question(request):
#     Question.objects.create(question_text="测试下sss反对法",
#                             pub_date="2023-05-29 12:21:13")
#     return HttpResponse("操作成功！")

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "PDFesc/detail.html", {"question": question})
