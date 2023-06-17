# YpoxreotikiErgasia23_E20132_Platanas_Evangelos

##### Πλατανάς Ευάγγελος - Ε20132
### Πληροφοριακά Συστήματα -Υποχρεωτική Εργασία 2023

## Δημιουργία Περιβάλλοντος
Για τη δημιουργία του περιβάλλοντος απαιτείται η λήψη του φακέλου flaskapp ο οποίος περιέχει ιεραρχικά τα παρακάτω αρχεία:

-flaskapp
  -docker-compose.yml
  -app
  -Dockerfile
  -digitalAirlines.py

Σε ένα terminal εκτελούμε τις εντολές:
1. sudo service docker start
2. sudo docker-compose build
3. sudo docker-compose up -d
4. ????????????Πηγαίνουμε στον φάκελο app και εκτελούμε python digitalAirlines.py 

Με αυτές τις εντολές θα δημιουργηθεί ένα container στο οποίο θα τρέξει το flask service, ένα container που θα τρέξει η βάση δεδομένων mongoDB και θα γίνει η σύνδεση μεταξύ τους.


## Τρόπος Λειτουργίας του Service
Υποθέτουμε ότι βρισκόμαστε στον /localhost:5000 στο Postman.

1. Εγγραφή στο σύστημα
  Η εγγραφή στο σύστημα γίνεται διαφορετικά για τους διαχειριστές και διαφορετικά για τους απλούς χρήστες.
  Στην περίπτωση των διαχειριστών η εγγραφή γίνεται κατευθείαν μέσω του MongoShell. Οδηγείες:
  1. Ανοίγουμε το terminal
  2. sudo docker start mongodb
  3. sudo docker exec -it mongodb mongosh
  4. use DigitalAirlines
  5. db.users.insertOne({"name":"<όνομα>", "surname":"<επώνυμο>", "email":"<email>", "password":"<κωδικός>", "dateOfBirth":"<dd/mm/yyyy>", "country":"<χώρα>", "passport":"<διαβατήριο>", "role":"admin"})
  
  Κατά την εγγραφή ενός διαχειριστή, το πεδίο "role" με τιμή "admin" είναι αυτό που τον καθιστά διαχειριστή. Για τους απλούς χρήστες η εγγραφή στο σύστημα γίνεται μέσω του endpoint /newRegistry (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος, της μορφής {"name":"<όνομα>", "surname":"<επώνυμο>", "email":"<email>", "password":"<κωδικός>", "dateOfBirth":"<dd/mm/yyyy>", "country":"<χώρα>", "passport":"<διαβατήριο>"}. Το πεδίο "role" παίρνει αυτόματα τη τιμή "simpleUser" που καθιστά τον συγκεκριμένο χρήστη απλό χρήστη.
    To email θα πρέπει να είναι μοναδικό!

  
2. Είσοδος στο σύστημα
  Η είσοδος στο σύστημα γίνεται μέσω του endpoint /login (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος που θα περιέχει τα πεδία "email" και "password", δηλαδή της μορφής {"email":"<email>, "password":"<password>"}. Αν το email και o κωδικός αντιστοιχούν σε κάποιον χρήστη τότε θα δίνεται authentication token (jwt). Προκειμένου να έχει πρόσβαση σε όλα τα υπόλοιπα endpoints (εκτός του /newRegistry και του /login) χρειάζεται να εισάγει το token αυτό ως argument στο URL. Το token δημιουργείται με βάση το ρόλο του χρήστη επομένως tokens που αντιστοιχούν σε απλούς χρήστες δεν μπορούν να χρησιμοποιηθούν για να γίνει πρόσβαση σε endpoints που χρησιμοποιούν μόνο οι διαχειριστές. Κάθε token έχει 1 ώρα ζωής, που σημαίνει ότι μετά το πέρας της μίας ώρας, ο χρήστης θα χρειαστεί να επαναλάβει τη διαδικασία εισόδου για να μπορεί να χρησιμοποιήσει το token του.

  
  3. Έξοδος από το σύστημα
  Η έξοδος από το σύστημα γίνεται μέσω του endpoint /logout?token=<token> (methods=['GET']). H έξοδος πραγματοποιείται ακυρώνοντας το token που εισήχθει ως argument στο URL. Ο χρήστης δεν θα μπορεί να το χρησιμοποιήσει για να έχει πρόσβαση στα endpoints του συστήματος και είναι αναγκασμένος να επαναλάβει τη διαδικασία εισόδου. Το token πρέπει να είναι ενεργό για να πραγματοποιηθεί μια έξοδος από το σύστημα!
  
  
  ##Στα παρακάτω endpoints έχουν πρόσβαση μόνο οι διαχειριστές
  
1. Προσθήκη πτήσης στη βάση δεδομένων
  Η προσθήκη μιας πτήσης γίνεται μέσω του endpoint /insertFlight?token=<token> (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος της μορφής {"from": "<from>", "to": "<to>", "date": "<dd/mm/yyyy>", "businessTickets": <πλήθος business εισητηρίων>, "businessPrice": <τιμή business εισητηρίων>, "economyTickets": <πλήθος economy εισητηρίων>, "economyPrice": <τιμή economy εισητηρίων>}. Τα πεδία "businessTickets", "businessPrice", "economyTickets" και "economyPrice" πρέπει να έχουν μια αριθμητική τιμή (όχι string).
  
  2. Ενημέρωση τιμής πτήσης
  Η ενημέρωση της τιμής μιας πτήσης γίνεται μέσω του endpoint /updatePrice?token=<token> (methods=['PUT']). Η ενημέρωση αυτή γίνεται με βάση του πεδίο "_id" κάθε πτήσης που δημιουργείται αυτόματα στη βάση δεδομένων (μόνο τους χαρακτήρες, όχι ολόκληρο το ObjectId). Επίσης πρέπει να αναφερθεί η κατηγορία εισητηρίου (business, economy ή και τα δύο) της οποίας η τιμή θα αλλάξει. Επομένως απαιτείται η εισαγωγή ενός json στο body του μηνύματος, της μορφής {"_id":"<_id>, <κατηγορία>:<νέα τιμή>}. Η νέα τιμή πρέπει να έχει αριθμητική τιμή (όχι string).
  
  3. Διαγραφή πτήσης
  Η διαγραφή μιας πτήσης γίνεται μέσω του endpoint /deleteFlight?token=<token> (methods=['DELETE']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος που θα περιέχει το "_id" της πτήσης, δηλαδή της μορφής {"_id":"<_id>"} Προκειμένου να γίνει η διαγραφή δεν πρέπει να έχει γίνει κάποια κράτηση στη συγκεκριμένη πτήση.
  
  
  ##Στα παρακάτω endpoints έχουν πρόσβαση μόνο οι απλοί χρήστες

  1. Κράτηση εισητηρίου
Η κράτηση εισητηρίου γίνεται μέσω του endpoint /ticketBooking?token=<token> (methods=['POST']). Απαιτείται ένα json της μορφής {"flightId": "<flightId>", "name": "<name>", "surname": "<surname>", "passport": "<passport>", "dateOfBirth": "<dd/mm/yyyy>", "email": "<email>", "ticketType": "<ticketType>"}. Το πεδίο "flightId" αφορά το μοναδικό _id της κράτησης στη βάση δεδομένων. Το "ticketType" πρέπει να έχει μια από τις τιμές "economy" ή "business", ενώ το email θα πρέπει να αντιστοιχεί στον χρήστη του οποίου το token χρησιμοποιήθηκε ως argument στο URL.

2. Εμφάνιση κρατήσεων χρήστη
   Η εμφάνιση των κρατήσεων ενός χρήστη γίνεται μέσω του endpoint /showBookings?token=<token> (methods=['GET']). Εμφανίζονται όλες οι κρατήσεις που έχουν γίνει με χρήση του email που αντιστοιχεί στο token.

   3. Εμφάνιση στοιχείων κράτησης
   Η εμφάνιση στοιχείων μιας συγκεκριμένης κράτησης του χρήστη γίνεται μέσω του endpoint /showBookingDetails?token=<token> (methods=['POST']). Απαιτείται εισαγωγή ενός json της μορφής {"_id":"<_id>"}, όπου "_id" είναι το μοναδικό _id της κράτησης το οποίο πρέπει να αντιστοιχεί σε κράτηση που έχει γίνει με email που συμβαδίζέι με το token.

4. Ακύρωση κράτησης
  Η ακύρωση κράτησης γίνεται μέσω του endpoint /deleteBooking?token=<token> (methods=['DELETE']). Απαιτείται εισαγωγή ενός json της μορφής {"_id":"<_id>"}, όπου "_id" είναι το μοναδικό _id της κράτησης το οποίο πρέπει να αντιστοιχεί σε κράτηση που έχει γίνει με email που συμβαδίζέι με το token.

5. Διαγραφή λογαριασμού
   Η διαγραφή λογαριασμού γίνεται μέσω του endpoint /deleteAccount?token=<token> (methods=['DELETE']). Διαγράφεται ο λογαριασμός στον οποίο αντιστοιχεί το token. 
  
  ##Στα παρακάτω endpoints έχουν πρόσβαση τόσο οι διαχειριστές όσο και οι απλοί χρήστες
  
  1. Αναζήτηση πτήσης
  Η αναζήτηση πτήσης γίνεται μέσω του endpoint /searchFlight?token=<token> (methods=['POST']). Η αναζήτηση μπορεί να γίνει με πολλούς τρόπους:
    Εισαγωγή ενός json της μορφής {"from":"<from>", "to":"<to>", "date":"<dd/mm/yyyy>"} επιστρέφει όλες τις πτήσεις με βάση το συγκεκριμένο αεροδρόμιο αναχώρησης, το συγκεκριμένο αεροδρόμιο προορισμού και τη συγκεκριμένη ημερομηνία
    Εισαγωγή ενός json της μορφής {"from":"<from>", "to":"<to>"} επιστρέφει όλες τις πτήσεις με βάση το συγκεκριμένο αεροδρόμιο αναχώρησης και το συγκεκριμένο αεροδρόμιο προορισμού
    Εισαγωγή ενός json της μορφής {"date":"<dd/mm/yyyy>"} επιστρέφει όλες τις πτήσεις με βάση  τη συγκεκριμένη ημερομηνία
  Εισαγωγή ενός κενού json, δηλαδή {}, επιστρέφει όλες τις διαθέσιμες πτήσεις
  
  
  2. Εμφάνιση στοιχείων πτήσης
  Η εμφάνιση των στοιχείων μιας πτήσης γίνεται μέσω του endpoint /showFlightDetails?token=<token> (methods=['POST']). Η αναζήτηση της πτήσης γίνεται με βάση το "_id", δηλαδή απαιτείται ένα json {"_id":"<_id>"}. Τα στοιχεία που εμφανίζονται για την πτήση είναι διαφορετικά σε περίπτωση που το token αντιστοιχεί σε έναν διαχειριστή και διαφορετικά σε περίπτωση που αντιστοιχεί σε απλό χρήστη.
  

   
  
