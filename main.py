from flask import Flask, render_template, request, redirect, send_file
from extractor.remoteok import extract_remoteok_jobs
from extractor.wwr import extract_wwr_jobs
from file import save_to_file

#create Flask application
app = Flask("JobScrapper")

#create cache(mini db) ex) 'python': [...]
db = {}


# decorator on top of the func >> visit / --> call func
@app.route("/")
def home():
    return render_template("home.html")


# search jobs w/template funcs
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_remoteok_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr
        # save results in db
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    #keyword를 입력했는지?
    if keyword == None:
        return redirect("/")
    #keyword를 검색했는지?
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
        #서버 파일시스템에 파일 저장
    save_to_file(keyword, db[keyword])
    #user가 파일 다운로드
    return send_file(f"{keyword}.csv", as_attachment=True)


#run webserver
app.run("0.0.0.0")
