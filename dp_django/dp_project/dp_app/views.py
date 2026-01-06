from django.shortcuts import render, redirect
from .models import History
import pandas as pd
import os
import joblib
from .models import PredictionHistory  # <- Import your model

from django.contrib import messages
from .models import Contact

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# 🔹 User login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('prediction')  # redirect to prediction after login
        else:
            return render(request, 'userlogin.html', {'error': 'Invalid username or password'})

    return render(request, 'user_login.html')


# 🔹 Signup (optional)
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists!'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('userlogin')

    return render(request, 'signup.html')


# 🔹 Home page (optional)
@login_required(login_url='user_login')
def home(request):
    return render(request, 'index.html')


# 🔹 Prediction page (only accessible after login)
@login_required(login_url='user_login')
def prediction(request):
    # your existing disease prediction logic here
    return render(request, 'prediction.html')


# 🔹 Logout
def user_logout(request):
    logout(request)
    return redirect('user_login')



path = os.path.dirname(__file__)
model = joblib.load(open(os.path.join(path, 'best_model.pkl'), 'rb'))
label_encoder = joblib.load(open(os.path.join(path, 'label_encode.pkl'), 'rb'))


def index(req):
    return render(req, 'index.html')




def prediction(req):
    if req.method == 'POST':
        fever = req.POST['fever']
        headache = req.POST['headache']
        nausea = req.POST['nausea']
        vomiting = req.POST['vomiting']
        fatigue = req.POST['fatigue']
        joint_pain = req.POST['joint_pain']
        skin_rash = req.POST['skin_rash']
        cough = req.POST['cough']
        weight_loss = req.POST['weight_loss']
        yellow_eyes = req.POST['yellow_eyes']

        symptoms = ['fever', 'headache', 'nausea', 'vomiting', 'fatigue',
                    'joint_pain', 'skin_rash', 'cough', 'weight_loss', 'yellow_eyes']
        user_input = [fever, headache, nausea, vomiting, fatigue,
                      joint_pain, skin_rash, cough, weight_loss, yellow_eyes]

        if all(val == '0' for val in user_input):
            return render(req, 'prediction.html', {'res': 'Please select at least one symptom.'})

        input_df = pd.DataFrame([user_input], columns=symptoms)
        prediction_result = model.predict(input_df)[0]
        predicted_value = label_encoder.inverse_transform([prediction_result])[0]

        if req.user.is_authenticated:
            PredictionHistory.objects.create(
                user=req.user,
                symptoms=", ".join([s for s, v in zip(symptoms, user_input) if v == '1']),
                predicted_disease=predicted_value
            )

        return render(req, 'prediction.html', {'res': predicted_value})

    return render(req, 'prediction.html')



@login_required(login_url='user_login')
def history(req):
    if req.user.is_authenticated:
        history = PredictionHistory.objects.filter(user=req.user).order_by('-created_at')
    else:
        history = []
    return render(req, 'history.html', {'history': history})


def upload_report(request):
    if request.method == 'POST':
        try:
            file = request.FILES['csv_file']
            df = pd.read_csv(file)

            expected_columns = ['fever', 'headache', 'nausea', 'vomiting', 'fatigue',
                                'joint_pain', 'skin_rash', 'cough', 'weight_loss', 'yellow_eyes']

            if not all(col in df.columns for col in expected_columns):
                raise ValueError("CSV must contain the required symptom columns.")

            results_list = []

            # Loop through each row in the CSV
            for i, row in df.iterrows():
                # Skip row if all symptoms are 0
                if all(int(val) == 0 for val in row[expected_columns]):
                    continue

                # Predict for this row
                input_row = row[expected_columns].values.reshape(1, -1)
                prediction_code = model.predict(input_row)[0]
                predicted_disease = label_encoder.inverse_transform([prediction_code])[0]

                # ✅ Prepare symptoms
                present_symptoms = [symptom for symptom, value in zip(expected_columns, row) if int(value) == 1]

                # ✅ Save to history with logged-in user and correct field name
                if request.user.is_authenticated:
                    PredictionHistory.objects.create(
                        user=request.user,
                        symptoms=", ".join(present_symptoms),
                        predicted_disease=predicted_disease
                    )

                # Add to results list for display
                results_list.append({
                    "symptoms": ", ".join(present_symptoms),
                    "prediction": predicted_disease
                })

            return render(request, 'upload_report.html', {'results_list': results_list})

        except Exception as e:
            return render(request, 'upload_report.html', {'error': f"Error processing file: {str(e)}"})

    return render(request, 'upload_report.html')



from django.shortcuts import get_object_or_404

def delete_history(request, id):
    if request.method == 'POST':
        record = get_object_or_404(PredictionHistory, id=id)
        record.delete()
    return redirect('history')

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

@csrf_exempt
def delete_all_history(request):
    if request.method == 'POST':
        PredictionHistory.objects.all().delete()
        return redirect('history')

def about_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process or save the contact message (e.g., send email or store in DB)
        # Optionally show a success message
    return render(request, 'aboutus.html')

from .models import ContactMessage

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, message=message)
        return render(request, 'aboutus.html', {'success': True})

    return render(request, 'aboutus.html')

from django.contrib.auth.decorators import login_required

@login_required
def contact_messages_view(request):
    messages = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'contact_messages.html', {'messages': messages})



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        return render(request, 'contactus.html', {'success': 'Message sent successfully!'})

    return render(request, 'contactus.html')


