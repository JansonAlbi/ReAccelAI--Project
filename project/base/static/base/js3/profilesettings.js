

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// Function to send OTP (simulated for demo)
function updatepassword(event) {
  event.preventDefault();
  
    // Simulate OTP generation and sending
    //alert("OTP sent successfully!");
    // Show OTP input field and Verify button
    //showOTPSection();
    const email = document.getElementById('email').value;
    if (email) {
        fetch('update_password_send_otp_ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ email: email })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                document.getElementById('entering-otp').style.display = 'block';
                //document.getElementById('otp').style.visibility = 'visible';
                document.getElementById('verify-otp').style.display = 'block';
                //showOTPSection();
                showModal("Successfully Sent Verification Code to Your Mail");
            }
            else {
              showModal("Failed to send OTP. Please try again.");
          }
        });
    }
          
}



function verify_otp(event) {
  //alert("fuck");
  //event.preventDefault();
    //verifying OTP
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;
    if (email && otp) {
        fetch('verify_otp_newpassword/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ email: email,otp: otp})
        }).then(response => response.json()).then(data => {
            if (data.success) {
                showModal("Mail verification successful");
                document.getElementById('newpassword_label').style.display = 'block';
                document.getElementById('newpassword').style.display = 'block';
                document.getElementById('confirmpassword_label').style.display = 'block';
                document.getElementById('confirm_password').style.display = 'block';
                document.getElementById('update_new_password').style.display = 'block';
            }
            else {
              showModal("Mail verification Failed");
          }
        });
    }
    else
    {
      showModal("inputs are incomplete");
    }
          
}



function new_password(event) {
    //alert("fuck");
    //event.preventDefault();
      //verifying OTP
      const email = document.getElementById('email').value;
      const new_password = document.getElementById('newpassword').value;
      const confirm_password = document.getElementById('confirm_password').value;
      const updating_newpassword=1;
      if (email && new_password && confirm_password && updating_newpassword) {
          fetch('updating_password_profile_settings/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken,
              },
              body: JSON.stringify({ email: email,new_password: new_password,confirm_password:confirm_password,updating_newpassword:updating_newpassword})
          }).then(response => response.json()).then(data => {
              if (data.success) {
                  showModal("Successfully Updated Your Password once Relogin & check it");
                  history.go(0);
                  
              }
              else {
                showModal("Updating Your New Password  Failed");
            }
          });
      }
      else
      {
        showModal("inputs are incomplete");
      }
            
  }



function showModal(message) {
  var modal = document.getElementById("myModal");
  var modalMessage = document.getElementById("modalMessage");
  modalMessage.textContent = message;
  modal.style.display = "block";
}

function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}

window.onclick = function(event) {
  var modal = document.getElementById("myModal");
  if (event.target == modal) {
      modal.style.display = "none";
  }
}