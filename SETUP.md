# Οδηγίες Εγκατάστασης - Exam Vault

## Βήμα 1: Εγκατάσταση Python Dependencies

```bash
pip install -r requirements.txt
```

## Βήμα 2: Ρύθμιση PostgreSQL

1. Εγκαταστήστε το PostgreSQL αν δεν το έχετε ήδη
2. Δημιουργήστε μια βάση δεδομένων:
```sql
CREATE DATABASE exam_vault;
```

## Βήμα 3: Ρύθμιση Environment Variables

Δημιουργήστε ένα αρχείο `.env` στον root φάκελο με το παρακάτω περιεχόμενο:

```env
SECRET_KEY=ΤΟ DJANGO ΚΛΕΙΔΙ ΣΑΣ
DEBUG=True
DB_NAME=exam_vault
DB_USER=postgres
DB_PASSWORD=Ο ΚΩΔΙΚΟΣ ΤΗΣ ΒΑΣΗΣ ΣΑΣ
DB_HOST=localhost
DB_PORT=5432
USE_S3=False
```

**Σημαντικό**: Αλλάξτε το `SECRET_KEY` και το `DB_PASSWORD` με τα δικά σας!

## Βήμα 4: Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Βήμα 5: Δημιουργία Superuser (Admin)

```bash
python manage.py createsuperuser
```

Θα σας ζητηθεί:
- Username
- Email (προαιρετικό)
- Password

## Βήμα 6: Εκκίνηση Server

```bash
python manage.py runserver
```

## Βήμα 7: Πρώτη Χρήση

1. **Admin Panel**: Πηγαίνετε στο `http://127.0.0.1:8000/admin/` και συνδεθείτε με τα credentials που δημιουργήσατε
2. **Προσθήκη Δεδομένων**:
   - Προσθέστε Πανεπιστήμια
   - Προσθέστε Μαθήματα
   - Προσθέστε Θέματα Εξέτασης
3. **Frontend**: Πηγαίνετε στο `http://127.0.0.1:8000/` για να δείτε την κύρια σελίδα

## Troubleshooting

### Σφάλμα σύνδεσης με PostgreSQL
- Ελέγξτε ότι το PostgreSQL τρέχει
- Ελέγξτε τα credentials στο `.env` file
- Βεβαιωθείτε ότι η βάση δεδομένων `exam_vault` έχει δημιουργηθεί

### Σφάλμα static files
- Εκτελέστε: `python manage.py collectstatic` (για production)

### Σφάλμα migrations
- Διαγράψτε το φάκελο `exams/migrations` (εκτός από `__init__.py`)
- Εκτελέστε ξανά: `python manage.py makemigrations` και `python manage.py migrate`


