# YpoxreotikiErgasia23_E20132_Platanas_Evangelos

### Πλατανάς Ευάγγελος - Ε20132
### Πληροφοριακά Συστήματα -Υποχρεωτική Εργασία 2023

Υποθέτουμε ότι βρισκόμαστε στον /localhost:5000 στο Postman.

1. Εγγραφή στο σύστημα
  Η εγγραφή στο σύστημα γίνεται διαφορετικά για τους διαχειριστές και διαφορετικά για τους απλούς χρήστες.
  Στην περίπτωση των διαχειριστών η εγγραφή γίνεται κατευθείαν μέσω του MongoShell. Οδηγείες:
  1. Ανοίγουμε το terminal
  2. sudo docker start mongodb
  3. sudo docker exec -it mongodb mongosh
  4. use DigitalAirlines
  5. db.users.insertOne({"name":"<όνομα>", "surname":"<επώνυμο>", "email":"<email>", "password":"<κωδικός>", "dateOfBirth":"<dd/mm/yyyy>", "country":"<χώρα>", "passport":"<διαβατήριο>", "role":"admin"})
  
  Κατά την εγγραφή ενός διαχειριστή, το πεδίο "role" με τιμή "admin" είναι αυτό που τον καθιστά διαχειριστή.
  
  Για τους απλούς χρήστες η εγγραφή στο σύστημα γίνεται μέσω του endpoint /newRegistry (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος που θα περιέχει τα πεδία "email" και "password" ({"email":"<email>, "password":"password"}). Αν το email και o κωδικός αντιστοιχούν σε κάποιον χρήστη τότε θα δίνεται ένα authentication token (jwt). Προκειμένου να έχει πρόσβαση σε όλα τα υπόλοιπα endpoints (εκτός του /login) χρειάζεται να εισάγει το token αυτό ως argument στο URL. Το δημιουργείται με βάση το ρόλο του χρήστη. 
  
