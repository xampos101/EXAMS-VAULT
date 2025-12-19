# 📚 Exam Vault - DUTH VAULT

Full-Stack Web Application για κεντρική βιβλιοθήκη παλαιών θεμάτων εξεταστικών περιόδων. Μια σύγχρονη πλατφόρμα που επιτρέπει στους φοιτητές να αναζητούν, προβάλλουν και κατεβάζουν θέματα εξετάσεων και σημειώσεις από διάφορα πανεπιστήμια.

## ✨ Χαρακτηριστικά

- 🔍 **Δυναμική Αναζήτηση**: Αναζήτηση μαθημάτων με φίλτρα (Πανεπιστήμιο, Τμήμα, Εξάμηνο, Κατηγορία)
- 📄 **Προβολή Αρχείων**: Προβολή PDF, εικόνων και άλλων εγγράφων απευθείας στον browser
- 📥 **Download**: Κατέβασμα αρχείων με ένα κλικ
- 🎨 **Σύγχρονο UI**: Modern, responsive interface με Tailwind CSS
- 🔐 **Admin Panel**: Πλήρης διαχείριση δεδομένων μέσω Django Admin
- 📱 **Responsive Design**: Λειτουργεί άψογα σε desktop, tablet και mobile

## 🚀 Τεχνική Στοίβα

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, Tailwind CSS, Vanilla JavaScript
- **Database**: PostgreSQL
- **File Storage**: django-storages (S3/Google Cloud Storage ready)
- **Python**: 3.8+

## 📋 Προαπαιτούμενα

Πριν ξεκινήσετε, βεβαιωθείτε ότι έχετε εγκαταστήσει:

- Python 3.8 ή νεότερη έκδοση
- PostgreSQL
- pip (Python package manager)

## 🔧 Εγκατάσταση

### 1. Clone το Repository

```bash
git clone https://github.com/xampos101/EXAMS-VAULT.git
cd EXAMS-VAULT
```

### 2. Δημιουργήστε Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Εγκαταστήστε τις Dependencies

```bash
pip install -r requirements.txt
```

### 4. Ρύθμιση PostgreSQL

Δημιουργήστε μια βάση δεδομένων PostgreSQL:

```sql
CREATE DATABASE exam_vault;
```

### 5. Δημιουργήστε το `.env` File

Δημιουργήστε ένα αρχείο `.env` στον root φάκελο με το παρακάτω περιεχόμενο:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=exam_vault
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
USE_S3=False
```

**Σημαντικό**: Αλλάξτε το `SECRET_KEY` και το `DB_PASSWORD` με τα δικά σας credentials!

### 6. Εκτελέστε Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Δημιουργήστε Superuser (Admin)

```bash
python manage.py createsuperuser
```

Θα σας ζητηθεί:
- Username
- Email (προαιρετικό)
- Password

### 8. Εκκινήστε τον Server

```bash
python manage.py runserver
```

Η εφαρμογή θα είναι διαθέσιμη στο: `http://127.0.0.1:8000/`

## 🎨 Χρήση

### Admin Panel

1. Πηγαίνετε στο `http://127.0.0.1:8000/admin/`
2. Συνδεθείτε με τα credentials που δημιουργήσατε
3. Προσθέστε:
   - **Πανεπιστήμια**: Όνομα και τοποθεσία
   - **Μαθήματα**: Όνομα, Πανεπιστήμιο, Τμήμα, Εξάμηνο, Κατηγορία
   - **Θέματα Εξέτασης**: Upload αρχείων (PDF, PNG, JPG, DOCX) με πληροφορίες εξεταστικής

### Frontend

1. Πηγαίνετε στο `http://127.0.0.1:8000/`
2. Χρησιμοποιήστε τα φίλτρα για να αναζητήσετε:
   - **Αναζήτηση**: Γράψτε το όνομα του μαθήματος
   - **Τύπος Εγγράφου**: Θέματα Εξεταστικής ή Σημειώσεις
   - **Πανεπιστήμιο**: Επιλέξτε πανεπιστήμιο
   - **Τμήμα**: Επιλέξτε τμήμα (μετά την επιλογή πανεπιστημίου)
   - **Εξάμηνο**: 1ο - 12ο
   - **Κατηγορία**: Υποχρεωτικό, Επιλογής, Εργαστήριο
3. **Εμφάνιση**: Κάντε κλικ στο "Εμφάνιση" για να δείτε το αρχείο στον browser
4. **Κατέβασμα**: Κάντε κλικ στο "Κατέβασμα" για να κατεβάσετε το αρχείο

## 📁 Δομή Project

```
EXAMS-VAULT/
├── exam_vault/          # Django project settings
│   ├── settings.py      # Project configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── exams/               # Main app
│   ├── models.py        # University, Subject, ExamPaper models
│   ├── admin.py         # Admin configuration
│   ├── views.py         # API endpoints & views
│   ├── urls.py          # App URL routing
│   └── migrations/     # Database migrations
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── exams/           # Exam-related templates
│       └── index.html   # Main page
├── static/              # Static files
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── media/               # Uploaded files (development)
│   └── exam_papers/     # Exam paper files
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── README.md           # This file
```

## 🔐 Δικαιώματα & Ασφάλεια

- **Admin Panel**: Μόνο οι συνδεδεμένοι διαχειριστές (superusers) έχουν πρόσβαση
- **File Upload**: Υποστηρίζονται μόνο PDF, PNG, JPG, JPEG, DOCX αρχεία
- **Public Access**: Το frontend είναι προσβάσιμο σε όλους, αλλά μόνο οι admins μπορούν να προσθέτουν/επεξεργάζονται δεδομένα

## ☁️ Production Deployment

### 🚀 Γρήγορο Deploy

Για να κάνετε deploy το application online (demo/production), ακολουθήστε τις οδηγίες στο **[DEPLOYMENT.md](DEPLOYMENT.md)**.

**Συνιστώμενες πλατφόρμες:**
- **Render.com** (δωρεάν, εύκολο) - [Οδηγίες](DEPLOYMENT.md#-rendercom-συνιστώμενη-λύση)
- **Railway.app** (δωρεάν credit) - [Οδηγίες](DEPLOYMENT.md#-alternative-railwayapp)

### 📋 Production Checklist

Για production deployment:

1. **Environment Variables**:
   ```env
   SECRET_KEY=your-super-secret-key
   DEBUG=False
   USE_S3=True  # Για static/media files
   ```

2. **AWS S3 Configuration** (για file storage):
   ```env
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=eu-central-1
   ```

3. **Security Settings**:
   - `DEBUG=False`
   - Ρυθμίστε `ALLOWED_HOSTS` στο `settings.py`
   - Χρησιμοποιείτε HTTPS
   - Ρυθμίστε backup για τη βάση δεδομένων

4. **Static Files**:
   - Εκτελέστε `python manage.py collectstatic`
   - Χρησιμοποιήστε CDN ή S3 για static files

## 🛠️ Ανάπτυξη

### Προσθήκη Νέων Χαρακτηριστικών

1. Κάντε fork το repository
2. Δημιουργήστε ένα branch για το feature σας (`git checkout -b feature/AmazingFeature`)
3. Κάντε commit τις αλλαγές σας (`git commit -m 'Add some AmazingFeature'`)
4. Push στο branch (`git push origin feature/AmazingFeature`)
5. Ανοίξτε ένα Pull Request

## 📝 Notes

- Το application υποστηρίζει PDF, PNG, JPG, JPEG, DOCX αρχεία
- Η αναζήτηση είναι case-insensitive
- Τα φίλτρα λειτουργούν δυναμικά (AJAX) χωρίς page refresh
- Η προβολή αρχείων γίνεται μέσω embedded viewer για PDF και εικόνες

## 👤 Developer

**xampos101**

- GitHub: [@xampos101](https://github.com/xampos101)
- Repository: [EXAMS-VAULT](https://github.com/xampos101/EXAMS-VAULT)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Framework
- Tailwind CSS
- PostgreSQL Community

---

Made with ❤️ by [xampos101](https://github.com/xampos101)

