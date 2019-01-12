<?php 

	$to = "contato@joaoemari.com.br"; // this is your Email address
	$from  = $_POST['email']; // this is the sender's Email address
	$sender_name = $_POST['name'];
	$number_of_guests = $_POST['guest'];
	$notes = $_POST['notes'];


	$subject = "RSVP";
	$message = $sender_name . " confirmou presença para " .  $number_of_guests . " e deixou a mensagem: ". "\n\n" . $notes;

	$headers = 'From: ' . $from;
	mail($to, $subject, $message, $headers);

?>