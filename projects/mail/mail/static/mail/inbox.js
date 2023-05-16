let current_mailbox = 'inbox';

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('', '', ''));

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').onsubmit = function() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;


    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })
    .then(() => {
      load_mailbox('sent');
    })
    .catch(error => {
        console.log('Error:', error);
    });

    return false;
  }
});

function compose_email(recipient, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function show_email(email_id) {

  // Show single email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      parent = document.querySelector('#email-view');
      parent.innerHTML = '';

      let emailDiv = document.createElement('div');

      let timestamp = document.createElement('div');
      timestamp.innerText = email['timestamp'];
      timestamp.className = 'email_timestamp';
      emailDiv.appendChild(timestamp);

      let sender = document.createElement('div');
      sender.innerText = `From: ${email['sender']}`;
      emailDiv.appendChild(sender);

      let recipients = document.createElement('div');
      recipients.innerText = `To: ${email['recipients']}`;
      emailDiv.appendChild(recipients);

      let subject = document.createElement('div');
      subject.innerText = email['subject'];
      subject.className = 'email_subject';
      emailDiv.appendChild(subject);

      let email_body = document.createElement('div');
      email_body.innerText = email['body'];
      emailDiv.appendChild(email_body);

      // Checking if this is an email that the user sent
      if (current_mailbox != 'sent') {

        // Adding the 'Archive' button
        let archive_button = document.createElement('button');
        archive_button.className = 'archive_button';
        let should_archive = true;
        if (email['archived']) {
          archive_button.innerText = 'Unarchive';
          should_archive = false;
        } else {
          archive_button.innerText = 'Archive';
          should_archive = true;
        };
        archive_button.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: should_archive
            })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
          })
          .then(() => {
            load_mailbox('inbox');
          })
          .catch(e => {
            console.log('Fetch error: ' + e.message);
          });
        });
        
        emailDiv.appendChild(archive_button);

        // Adding the 'Reply' button
        let reply_button = document.createElement('button');
        reply_button.innerText = 'Reply';
  
        // Creating the reply subject
        let reply_subject = '';
        if (email.subject.includes('Re:')) {
          reply_subject = email.subject;
        } else {
          reply_subject = `Re: ${email.subject}`;
        }
  
        // Creating the reply body
        let reply_body = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`
        
        reply_button.addEventListener('click', function() {
          compose_email(email.sender, reply_subject, reply_body)
        });
        
        emailDiv.appendChild(reply_button);
      }

      parent.append(emailDiv);
  });

}

function load_mailbox(mailbox) {
  current_mailbox = mailbox;
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;'Timestamp'

  
  // Create a new flex container
  let container = document.createElement('div');
  container.className = 'email-container';

  // Get the emails from API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Show the emails
      emails.forEach(email => {
        let emailDiv = document.createElement('div');
        emailDiv.className = 'email';
        if (email.read === true && mailbox != 'sent') {
          emailDiv.className = 'email email-read'
        }

        let date = new Date(email.timestamp);
        email.timestamp = date.getMonth() + '/' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes();
                
        ['timestamp', 'subject', 'sender'].forEach(key => {
            let element = document.createElement('div');
            element.innerText = email[key];
            if (key === 'subject') {
              element.className = 'subject';
            }
            emailDiv.appendChild(element);
        });

        emailDiv.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          show_email(email.id);
        });

        container.appendChild(emailDiv);
      });

      document.querySelector('#emails-view').append(container);

  });
}
