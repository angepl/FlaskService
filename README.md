# FlaskService

## Δημιουργία Περιβάλλοντος
Για τη δημιουργία του περιβάλλοντος απαιτείται η λήψη του φακέλου flaskapp ο οποίος περιέχει ιεραρχικά τα παρακάτω αρχεία:

- flaskapp
  - docker-compose.yml
  - app
    - Dockerfile
    - digitalAirlines.py

Σε ένα terminal εκτελούμε τις εντολές (βρισκόμενοι στον φάκελο flaskapp):
1. `sudo service docker start` 
2. `sudo docker-compose build` ή `sudo docker compose build`
3. `sudo docker-compose up -d` ή `sudo docker compose up -d`

Με αυτές τις εντολές θα δημιουργηθεί ένα container στο οποίο θα τρέξει το flask service, ένα container που θα τρέξει η βάση δεδομένων mongoDB και θα γίνει η σύνδεση μεταξύ τους.

Αν τα παραπάνω δεν λειτουργήσουν, ίσως χρειάζεται να εκτελεστούν πρώτα οι εντολές:
1. `sudo iptables -A INPUT -p tcp --dport 27017 -j ACCEPT`
2.  `sudo ufw allow 27017`

## Τρόπος Λειτουργίας του Service
Υποθέτουμε ότι βρισκόμαστε στον /localhost:5000 στο Postman.

### 1. Εγγραφή στο σύστημα

Η εγγραφή στο σύστημα γίνεται διαφορετικά για τους διαχειριστές και διαφορετικά για τους απλούς χρήστες.
Στην περίπτωση των διαχειριστών η εγγραφή γίνεται κατευθείαν μέσω του MongoShell. Οδηγίες:
1. Ανοίγουμε το terminal
2. `sudo docker start mongodb`
3. `sudo docker exec -it mongodb mongosh`
4. `use DigitalAirlines`
5. `db.users.insertOne({"name":"<όνομα>", "surname":"<επώνυμο>", "email":"<email>", "password":"<κωδικός>", "dateOfBirth":"<dd/mm/yyyy>", "country":"<χώρα>", "passport":"<διαβατήριο>", "role":"admin"})`
  
Κατά την εγγραφή ενός διαχειριστή, το πεδίο *role* με τιμή *admin* είναι αυτό που τον καθιστά διαχειριστή. Για τους απλούς χρήστες η εγγραφή στο σύστημα γίνεται μέσω του endpoint /newRegistry (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος, της μορφής `{"name":"<όνομα>", "surname":"<επώνυμο>", "email":"<email>", "password":"<κωδικός>", "dateOfBirth":"<dd/mm/yyyy>", "country":"<χώρα>", "passport":"<διαβατήριο>"}`. Το πεδίο *role* παίρνει αυτόματα τη τιμή *simpleUser* που καθιστά τον συγκεκριμένο χρήστη απλό χρήστη. **To email θα πρέπει να είναι μοναδικό!**

Παράδειγμα:

![newRegistry](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/ee6fe536-fc30-4c10-aff8-25d8bd22b916)

  
### 2. Είσοδος στο σύστημα

Η είσοδος στο σύστημα γίνεται μέσω του endpoint /login (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος που θα περιέχει τα πεδία *email* και *password*, δηλαδή της μορφής `{"email":"<email>", "password":"<password>"}`. Αν το email και o κωδικός αντιστοιχούν σε κάποιον χρήστη τότε θα δίνεται authentication token (jwt). Προκειμένου ο χρήστης να έχει πρόσβαση σε όλα τα υπόλοιπα endpoints (εκτός του /newRegistry και του /login) χρειάζεται να εισάγει το token αυτό ως argument στο URL. Το token δημιουργείται με βάση το ρόλο του χρήστη, επομένως tokens που αντιστοιχούν σε απλούς χρήστες δεν μπορούν να χρησιμοποιηθούν για να γίνει πρόσβαση σε endpoints που χρησιμοποιούν μόνο οι διαχειριστές και το ανάποδο. Επίσης κατά τη δημιουργία του token εισάγεται ως παράμετρος και το email του χρήστη. Κάθε token έχει 1 ώρα ζωής, που σημαίνει ότι μετά το πέρας της μίας ώρας, ο χρήστης θα χρειαστεί να επαναλάβει τη διαδικασία εισόδου για να μπορεί να έχει πρόσβαση στα endpoints που δικαιούται να προσπελάσει.

Παράδειγμα:

![login](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/190e272d-e7b1-4bd2-bfe1-aa4eb3cc92f3)


### 3. Έξοδος από το σύστημα

Η έξοδος από το σύστημα γίνεται μέσω του endpoint /logout?token=*token* (methods=['GET']). H έξοδος πραγματοποιείται ακυρώνοντας το token που εισήχθει ως argument στο URL. Ο χρήστης δεν θα μπορεί να το χρησιμοποιήσει για να έχει πρόσβαση στα endpoints του συστήματος και είναι αναγκασμένος να επαναλάβει τη διαδικασία εισόδου. **Το token πρέπει να είναι ενεργό για να πραγματοποιηθεί μια έξοδος από το σύστημα!**

Παράδειγμα:

![logout](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/98ee0346-41f7-492a-b6a3-2f4256c18e80)
  
  
### 4. Προσθήκη πτήσης στη βάση δεδομένων (μόνο για τους διαχειριστές)

Η προσθήκη μιας πτήσης γίνεται μέσω του endpoint /insertFlight?token=*token* (methods=['POST']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος της μορφής `{"from": "<from>", "to": "<to>", "date": "<dd/mm/yyyy>", "businessTickets": <πλήθος business εισητηρίων>, "businessPrice": <τιμή business εισητηρίων>, "economyTickets": <πλήθος economy εισητηρίων>, "economyPrice": <τιμή economy εισητηρίων>}`. **Τα πεδία *businessTickets*, *businessPrice*, *economyTickets* και *economyPrice* πρέπει να έχουν μια αριθμητική τιμή (όχι string).**

Παράδειγμα:

![insertFlight](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/49a8aa67-0359-4e38-9c7d-fb4f81ca9bfb)

  
### 5. Ενημέρωση τιμής πτήσης (μόνο για τους διαχειριστές)

Η ενημέρωση της τιμής μιας πτήσης γίνεται μέσω του endpoint /updatePrice?token=*token* (methods=['PUT']). Η ενημέρωση αυτή γίνεται με βάση του πεδίο *_id* κάθε πτήσης που δημιουργείται αυτόματα στη βάση δεδομένων (μόνο τους χαρακτήρες, όχι ολόκληρο το ObjectId). Επίσης πρέπει να αναφερθεί η κατηγορία εισητηρίου (businessPrice, economyPrice ή και τα δύο) της οποίας η τιμή θα αλλάξει. Επομένως απαιτείται η εισαγωγή ενός json στο body του μηνύματος, της μορφής `{"_id":"<_id>", "<κατηγορία>":<νέα τιμή>}`. **Το πεδίο *κατηγορία* πρέπει να έχει μία από τις τιμές *businessPrice* ή *economyPrice*. Η νέα τιμή πρέπει να έχει αριθμητική τιμή (όχι string).**

Παράδειγμα:

![updatePrice](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/8065db29-4f48-45ce-97fb-0a2faeff9829)

  
### 6. Διαγραφή πτήσης (μόνο για τους διαχειριστές)

Η διαγραφή μιας πτήσης γίνεται μέσω του endpoint /deleteFlight?token=*token* (methods=['DELETE']). Απαιτείται η εισαγωγή ενός json στο body του μηνύματος που θα περιέχει το *_id* της πτήσης, δηλαδή της μορφής `{"_id":"<_id>"}`. **Προκειμένου να γίνει η διαγραφή δεν πρέπει να έχει γίνει κάποια κράτηση στη συγκεκριμένη πτήση.**

Παράδειγμα:

![deleteFlight](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/989a0566-b762-48c3-8891-dea3a47c7efc)
  

### 7. Κράτηση εισητηρίου (μόνο για απλούς χρήστες)

Η κράτηση εισητηρίου γίνεται μέσω του endpoint /ticketBooking?token=*token* (methods=['POST']). Απαιτείται ένα json της μορφής `{"flightId": "<flightId>", "name": "<name>", "surname": "<surname>", "passport": "<passport>", "dateOfBirth": "<dd/mm/yyyy>", "email": "<email>", "ticketType": "<ticketType>"}`. Το πεδίο *flightId* αφορά το μοναδικό _id της πτήσης στη βάση δεδομένων. **Το *ticketType* πρέπει να έχει μια από τις τιμές *economy* ή *business*, ενώ το email θα πρέπει να αντιστοιχεί στον χρήστη του οποίου το token χρησιμοποιήθηκε ως argument στο URL.**

Παράδειγμα:

![ticketBooking](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/f297d73a-5b88-4916-b6f2-815c28269def)


### 8. Εμφάνιση κρατήσεων χρήστη (μόνο για απλούς χρήστες)

Η εμφάνιση των κρατήσεων ενός χρήστη γίνεται μέσω του endpoint /showBookings?token=*token* (methods=['GET']). Εμφανίζονται όλες οι κρατήσεις που έχουν γίνει με χρήση του email που αντιστοιχεί στο token.

Παράδειγμα:

![showBookings](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/0091d9f3-91dd-4972-bfcc-c05de022d3b8)


### 9. Εμφάνιση στοιχείων κράτησης (μόνο για απλούς χρήστες)

Η εμφάνιση στοιχείων μιας συγκεκριμένης κράτησης του χρήστη γίνεται μέσω του endpoint /showBookingDetails?token=*token* (methods=['POST']). Απαιτείται εισαγωγή ενός json της μορφής `{"_id":"<_id>"}`, όπου *_id* είναι το μοναδικό _id της κράτησης το οποίο πρέπει να αντιστοιχεί σε κράτηση που έχει γίνει με email που συμβαδίζει με το token.

Παράδειγμα:

![showBookingDetails](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/528b711b-a309-48dd-9ae3-8c7cb140ea63)


### 10. Ακύρωση κράτησης (μόνο για απλούς χρήστες)

Η ακύρωση κράτησης γίνεται μέσω του endpoint /deleteBooking?token=*token* (methods=['DELETE']). Απαιτείται εισαγωγή ενός json της μορφής `{"_id":"<_id>"}`, όπου *_id* είναι το μοναδικό _id της κράτησης το οποίο πρέπει να αντιστοιχεί σε κράτηση που έχει γίνει με email που συμβαδίζει με το token.

Παράδειγμα:

![deleteBooking](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/e01ca0b9-60a1-4360-a87b-622f090fb1e7)


### 11. Διαγραφή λογαριασμού (μόνο για απλούς χρήστες)

Η διαγραφή λογαριασμού γίνεται μέσω του endpoint /deleteAccount?token=*token* (methods=['DELETE']). Διαγράφεται ο λογαριασμός στον οποίο αντιστοιχεί το token (μέσω του οποίου γίνεται αναγνώριση του email και άρα της εγγραφή στη βάση δεδομένων). 

Παράδειγμα:

![deleteAccount](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/40170744-94e0-4afe-9839-1cba4b3054de)

  
### 12. Αναζήτηση πτήσης (για διαχειριστές και απλούς χρήστες)

Η αναζήτηση πτήσης γίνεται μέσω του endpoint /searchFlight?token=*token* (methods=['POST']). Η αναζήτηση μπορεί να γίνει με πολλούς τρόπους:
  - Εισαγωγή ενός json της μορφής `{"from":"<from>", "to":"<to>", "date":"<dd/mm/yyyy>"}` επιστρέφει όλες τις πτήσεις με βάση το συγκεκριμένο αεροδρόμιο αναχώρησης, το συγκεκριμένο αεροδρόμιο προορισμού και τη συγκεκριμένη ημερομηνία
  - Εισαγωγή ενός json της μορφής `{"from":"<from>", "to":"<to>"}` επιστρέφει όλες τις πτήσεις με βάση το συγκεκριμένο αεροδρόμιο αναχώρησης και το συγκεκριμένο αεροδρόμιο προορισμού
  - Εισαγωγή ενός json της μορφής `{"date":"<dd/mm/yyyy>"}` επιστρέφει όλες τις πτήσεις με βάση  τη συγκεκριμένη ημερομηνία
  - Εισαγωγή ενός κενού json, δηλαδή `{}`, επιστρέφει όλες τις διαθέσιμες πτήσεις

Παράδειγμα:

![searchFlight](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/0e48c473-9782-47f5-b5a2-c242e5398af2)
  
  
### 13. Εμφάνιση στοιχείων πτήσης (για διαχειριστές και απλούς χρήστες)

Η εμφάνιση των στοιχείων μιας πτήσης γίνεται μέσω του endpoint /showFlightDetails?token=*token* (methods=['POST']). Η αναζήτηση της πτήσης γίνεται με βάση το *_id*, δηλαδή απαιτείται ένα json `{"_id":"<_id>"}`. **Τα στοιχεία που εμφανίζονται για την πτήση είναι διαφορετικά σε περίπτωση που το token αντιστοιχεί σε έναν διαχειριστή και διαφορετικά σε περίπτωση που αντιστοιχεί σε απλό χρήστη.**

Παράδειγμα για απλό χρήστη:

![showFlightDetails_simpleUser](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/2de872fa-8552-4025-b626-cdf202630ef1)

Παράδειγμα για διαχειριστή:

![showFlightDetails_admin](https://github.com/angepl/YpoxreotikiErgasia23_E20132_Platanas_Evangelos/assets/121619065/605da841-5944-4398-86c3-8dbdaa73663c)
  

   
  
