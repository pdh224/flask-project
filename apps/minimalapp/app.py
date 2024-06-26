# from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email, EmailNotValidError
from flask import (Flask, current_app, g, render_template, url_for,request,redirect,flash)
import logging
import os
from flask_mail import Mail,Message

#  서버 프로그램 객체를 만든다
# __name__: 실행 중인 모듈의 시스템 상의 이름


app=Flask(__name__)
# 기본 주소로 요청이 왔을 때  무엇을 할지 정의하기

app.config["SECRET_KEY"]="2AZSMss3p5QPbcY2hBsJ"

# app.config["DEBUG_TB_INTERCEPT_REDIRECT"]=False
# toolbar=DebugToolbarExtension(app)

app.config["MAIL_SERVER"]=os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"]=os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"]=os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"]=os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"]=os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"]=os.environ.get("MAIL_DEFAULT_SENDER")
mail= Mail(app)




@app.route("/")
def index():
    return "Hello, Flask"

# 메소드에 따른 처리를 원한다면 구별하여 정의할 수 있다.

@app.route("/hello/<name>")
def hello(name):
    return f'Hello, {name}!!'

@app.route("/name/<name>")
def show_name(name):
    # 변수를 템플릿 엔진에게 건넨다
    return render_template("index.html",name=name)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello",name="world"))
    print(url_for("show_name", name="nm",page="1"))
    

#플라스크의 템플릿 문서는 앱 내 templates 폴더에 있다고 가정한다.
@app.route("/contact")
def contact():
    return render_template("contact.html")

#post 요청이 오면, 필요한 데이터 관련 처리를 하고나서 contact_complete.html템플릿을 주는 get 처리를 하면서 마무리
@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        #form 속성을 사용해서 폼의 값을 취득한다
        username= request.form["username"]
        email=request.form["email"]
        description=request.form["description"]
        
        #입력 체크
        is_vaild=True
        if not username:
            flash("사용자명은 필수입니다")
            is_vaild=False
        if not email:
            flash("메일 주소는 필수입니다")
            is_vaild=False
        try:
            validate_email(email)#이메일 형식 검사
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_vaild=False
        
        if not description:
            flash("문의 내용은 필수입니다")
            is_vaild=False

        if not is_vaild:
            return redirect(url_for("contact"))
        
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )



        #이메일을 보낸다(나중에 구현할 부분)
        flash("문의해 주셔서 감사합니다")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    #메일을 송신하는 함수
    msg=Message(subject,recipients=[to])
    msg.body=render_template(template + ".txt",**kwargs)
    msg.html=render_template(template + ".html",**kwargs)
    mail.send(msg)