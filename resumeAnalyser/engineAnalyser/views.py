import time, datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from pyresparser import ResumeParser
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import os
from fpdf import FPDF

from .forms import FileFieldForm
from .models import ResumeModel
from .utils import *
from PyPDF2 import PdfReader


# Create your views here.


def index(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ResumeModel(resume=request.FILES['file'], name=request.FILES['file'].name)
            instance.save()
            res_data = ResumeParser(os.path.join(settings.MEDIA_ROOT, 'resumes', instance.name)).get_extracted_data()
            reader = PdfReader(instance.resume)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text() + "\n"

            if res_data:
                pdf = FPDF()
                pdf.add_page()

                # set style and size of font
                # that you want in the pdf
                pdf.set_font("Arial", size=15)

                pdf.set_title("**Resume Analysis**")

                write_one_line_into_pdf(pdf, "Hello " + str(res_data['name']), "L")
                write_one_line_into_pdf(pdf, "**Your Basic info**", "L")
                try:
                    write_one_line_into_pdf(pdf, 'Name: ' + res_data['name'], "L")
                    write_one_line_into_pdf(pdf, 'Email: ' + res_data['email'], "L")
                    write_one_line_into_pdf(pdf, 'Contact: ' + res_data['mobile_number'], "L")
                    write_one_line_into_pdf(pdf, 'Resume pages: ' + res_data['no_of_pages'], "L")
                except Exception as e:
                    print(e)
                    pass
                cand_level = ''
                if res_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    write_one_line_into_pdf(pdf, "You are looking Fresher.</h4>", "L")

                elif res_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    write_one_line_into_pdf(pdf, "You are at intermediate level!", "L")

                elif res_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    write_one_line_into_pdf(pdf, "You are at experience level!", "L")

                pdf.add_page()
                pdf.set_title("**Skills Recommendation**")
                # write_one_line_into_pdf(pdf, "**Skills Recommendation**", "C")

                # Skill shows
                write_one_line_into_pdf(pdf, "Skills that you have!", "C")
                write_one_line_into_pdf(pdf, res_data['skills'], "L")

                # recommendation
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                              'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in res_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:

                        reco_field = 'Data Science'
                        write_one_line_into_pdf(pdf, "\n\n\n** Our analysis says you are looking for Data Science Jobs.**",
                                                "C")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                              'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                              'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                              'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                              'Streamlit']
                        write_one_line_into_pdf(pdf, "### Recommended skills for you.(Generated from system)", "C")
                        write_one_line_into_pdf(pdf, recommended_skills, "L")


                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        
                        reco_field = 'Web Development'
                        write_one_line_into_pdf(pdf, "\n\n\n** Our analysis says you are looking for Web Development Jobs **",
                                                "C")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                              'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']

                        write_one_line_into_pdf(pdf, "\n\n\n### Recommended skills for you.(Generated from system)", "C")
                        write_one_line_into_pdf(pdf, recommended_skills, "L")


                    ## Android App Development
                    elif i.lower() in android_keyword:
                        
                        reco_field = 'Android Development'
                        write_one_line_into_pdf(pdf,
                                                "\n\n\n** Our analysis says you are looking for Android App Development Jobs **",
                                                "C")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                              'Kivy', 'GIT', 'SDK', 'SQLite']

                        write_one_line_into_pdf(pdf, "\n\n\n### Recommended skills for you.(Generated from system)", "C")
                        write_one_line_into_pdf(pdf, recommended_skills, "L")

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        
                        reco_field = 'IOS Development'
                        write_one_line_into_pdf(pdf,
                                                "\n\n\n** Our analysis says you are looking for IOS App Development Jobs **",
                                                "C")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                              'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                              'Auto-Layout']

                        write_one_line_into_pdf(pdf, "### Recommended skills for you.(Generated from system)", "C")
                        write_one_line_into_pdf(pdf, recommended_skills, "L")

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        
                        reco_field = 'UI-UX Development'
                        write_one_line_into_pdf(pdf,
                                                "\n\n\n** Our analysis says you are looking for UI-UX Development Jobs **",
                                                "C")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                              'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                              'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                              'Solid', 'Grasp', 'User Research']

                        write_one_line_into_pdf(pdf, "### Recommended skills for you.(Generated from system)", "C")
                        write_one_line_into_pdf(pdf, recommended_skills, "L")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)


                ### Resume writing recommendation
                pdf.add_page()
                pdf.set_title("**Resume Tips & Ideas**")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score = resume_score + 20
                    write_one_line_into_pdf(pdf, "### Awesome! You have added Objective", "C")
                else:
                    write_one_line_into_pdf(pdf, "According to our recommendation please add your career objective, it will give your career intension to the Recruiters", "C")
                if 'Declaration' in resume_text:
                    resume_score = resume_score + 20
                    write_one_line_into_pdf(pdf, "### Awesome! You have added Declaration!", "C")
                else:
                    write_one_line_into_pdf(pdf, "According to our recommendation please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you", "C")

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    write_one_line_into_pdf(pdf, "### Awesome! You have added Declaration!", "C")
                else:
                    write_one_line_into_pdf(pdf,
                                            "### According to our recommendation please add Hobbies. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not",
                                            "C")

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    write_one_line_into_pdf(pdf, "### Awesome! You have added Achievements!", "C")
                else:
                    write_one_line_into_pdf(pdf, "### According to our recommendation please add Achievements. It will show that you are capable for the required position.", "C")

                if 'Projects' in resume_text:
                    resume_score = resume_score + 20
                    write_one_line_into_pdf(pdf, "### Awesome! You have added Projects!", "C")
                else:
                    write_one_line_into_pdf(pdf,
                                            "### According to our recommendation please add Projects. It will show that you have done work related the required position or not.",
                                            "C")

                pdf.add_page()
                pdf.set_title("**Resume Score**")

                write_one_line_into_pdf(pdf, "### Awesome! ** Your Resume Writing Score: " + str(resume_score) + "/100",  "C")
                write_one_line_into_pdf(pdf, "** Note: This score is calculated based on the content that you have added in your Resume. **", "l")

                print("SCORE? ")
                write_one_line_into_pdf(pdf, "Generated at: " + str(timestamp), "L")


                # results_path =  "C:\\Users\\mariu\\Desktop\\NLP_Project\\resumeAnalyser\\staticfiles\\media\\results"
                pdf.output(name="C:\\Users\\mariu\\Desktop\\NLP_Project\\resumeAnalyser\\staticfiles\\media\\results\\result_"+instance.name, dest='F')

            else:
                print('Something went wrong..')  # show in web using messages django class

            request.session['resume_name'] = instance.name
            print(instance.name)
            return redirect("results")
        else:
            print("FORM ERRORS:" + form.errors)
    else:

        form = FileFieldForm()
    return render(request, 'index.html', {'form': form})


def results(request):
    return render(request, 'results.html', context=None)


def about(request):
    context = {"uni": "Universitatea Bucuresti", "prof": "Profesor Dinu Anca", "masterand": "Radu Marius"}
    return render(request, 'about.html', context=context)
