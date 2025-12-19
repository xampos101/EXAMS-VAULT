# 🚀 Οδηγίες Deployment - Exam Vault

Αυτός ο οδηγός θα σας βοηθήσει να κάνετε deploy το Exam Vault application στο Render.com (δωρεάν hosting για Django apps).

## ⚠️ Σημαντικό

Το **GitHub Pages** υποστηρίζει μόνο static websites (HTML/CSS/JS) και **ΔΕΝ** μπορεί να τρέξει Django applications. Για Django apps χρειάζεστε έναν server που υποστηρίζει Python.

## 🌐 Render.com (Συνιστώμενη Λύση)

Το Render.com προσφέρει δωρεάν hosting για Django applications με PostgreSQL database.

### Βήμα 1: Προετοιμασία Repository

1. Βεβαιωθείτε ότι όλα τα αρχεία είναι committed στο GitHub:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Βήμα 2: Δημιουργία Account στο Render.com

1. Πηγαίνετε στο [render.com](https://render.com)
2. Κάντε sign up με GitHub account (πιο εύκολο)
3. Συνδέστε το GitHub repository σας

### Βήμα 3: Δημιουργία PostgreSQL Database

1. Στο Render Dashboard, κάντε κλικ στο **"New +"** → **"PostgreSQL"**
2. Ονομάστε το: `exam-vault-db`
3. Επιλέξτε **Free** plan
4. Κάντε κλικ **"Create Database"**
5. Αναμένετε να ολοκληρωθεί η δημιουργία (2-3 λεπτά)

### Βήμα 4: Δημιουργία Web Service

1. Στο Render Dashboard, κάντε κλικ στο **"New +"** → **"Web Service"**
2. Συνδέστε το GitHub repository σας (`xampos101/EXAMS-VAULT`)
3. Συμπληρώστε:
   - **Name**: `exam-vault` (ή ό,τι θέλετε)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```bash
     gunicorn exam_vault.wsgi:application
     ```
   - **Plan**: `Free`

### Βήμα 5: Ρύθμιση Environment Variables

Στο Web Service που μόλις δημιουργήσατε, πηγαίνετε στο tab **"Environment"** και προσθέστε:

```
SECRET_KEY=your-super-secret-key-here-min-50-chars
DEBUG=False
DB_NAME=exam_vault
DB_USER=<από το PostgreSQL database>
DB_PASSWORD=<από το PostgreSQL database>
DB_HOST=<από το PostgreSQL database>
DB_PORT=5432
USE_S3=False
```

**Σημαντικό**: 
- Το `SECRET_KEY` πρέπει να είναι ένα τυχαίο string (μπορείτε να χρησιμοποιήσετε [αυτό το generator](https://djecrety.ir/))
- Τα `DB_USER`, `DB_PASSWORD`, `DB_HOST` τα βρίσκετε στο PostgreSQL database settings στο Render

### Βήμα 6: Deploy

1. Κάντε κλικ **"Create Web Service"**
2. Το Render θα ξεκινήσει το build process (5-10 λεπτά)
3. Αφού ολοκληρωθεί, θα έχετε ένα URL τύπου: `https://exam-vault.onrender.com`

### Βήμα 7: Database Migrations & Superuser

Μετά το πρώτο deploy:

1. Πηγαίνετε στο **"Shell"** tab του Web Service
2. Εκτελέστε:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Βήμα 8: Προσθήκη Δεδομένων

1. Πηγαίνετε στο `https://your-app.onrender.com/admin/`
2. Συνδεθείτε με τα credentials που δημιουργήσατε
3. Προσθέστε Πανεπιστήμια, Μαθήματα και Θέματα Εξέτασης

## 🔄 Automatic Deployments

Το Render κάνει αυτόματο deploy κάθε φορά που κάνετε push στο main branch του GitHub repository.

## 📝 Alternative: Railway.app

Αν προτιμάτε Railway:

1. Πηγαίνετε στο [railway.app](https://railway.app)
2. Κάντε sign up με GitHub
3. Κάντε **"New Project"** → **"Deploy from GitHub repo"**
4. Επιλέξτε το repository σας
5. Προσθέστε PostgreSQL service
6. Ρυθμίστε environment variables
7. Railway θα κάνει auto-deploy!

## 🆓 Free Tier Limitations

**Render.com Free Tier:**
- ⚠️ Ο server "κοιμάται" μετά από 15 λεπτά αδράνειας
- ⚠️ Το πρώτο request μετά το "κοιμάτι" μπορεί να πάρει 30-60 δευτερόλεπτα
- ✅ Unlimited requests όταν είναι active
- ✅ 750 ώρες/μήνα (αρκετό για demo)

**Railway.app Free Tier:**
- ⚠️ $5 credit/μήνα (αρκετό για μικρά projects)
- ✅ Δεν "κοιμάται" όπως το Render

## 🎯 Production Tips

Για production deployment:

1. **Static Files**: Χρησιμοποιήστε S3 ή Cloudflare R2
2. **Media Files**: Χρησιμοποιήστε S3 για τα exam papers
3. **Domain**: Μπορείτε να προσθέσετε custom domain
4. **HTTPS**: Ενεργό αυτόματα στο Render/Railway
5. **Backups**: Ρυθμίστε automatic backups για τη βάση

## 🐛 Troubleshooting

### Build Fails
- Ελέγξτε τα logs στο Render dashboard
- Βεβαιωθείτε ότι όλα τα dependencies είναι στο `requirements.txt`
- Ελέγξτε ότι το `gunicorn` είναι στα requirements

### Database Connection Error
- Ελέγξτε τα environment variables
- Βεβαιωθείτε ότι το PostgreSQL database είναι running
- Ελέγξτε ότι τα credentials είναι σωστά

### Static Files Not Loading
- Ελέγξτε ότι το `collectstatic` τρέχει στο build command
- Βεβαιωθείτε ότι το `STATIC_ROOT` είναι σωστά ρυθμισμένο

## 📚 Χρήσιμοι Σύνδεσμοι

- [Render.com Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://gunicorn.org/)

---

**Ερωτήσεις?** Ανοίξτε ένα issue στο [GitHub Repository](https://github.com/xampos101/EXAMS-VAULT)


