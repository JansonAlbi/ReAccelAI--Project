const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Replace with actual data or API call
const countryCodes = [
  { code: 'United States', name: '+1' },
  { code: 'United Kingdom', name: '+44' },
  { code: 'China', name: '+86' },
  { code: 'India', name: '+91' },
  { code: 'France', name: '+33' },
  { code: 'Germany', name: '+49' },
  { code: 'Japan', name: '+81' },
  { code: 'Brazil', name: '+55' },
  { code: 'Russia', name: '+7' },
  { code: 'South Africa', name: '+27' },
  { code: 'Canada', name: '+1' },
  { code: 'Australia', name: '+61' },
  { code: 'Italy', name: '+39' },
  { code: 'Spain', name: '+34' },
  { code: 'Mexico', name: '+52' },
  { code: 'Indonesia', name: '+62' },
  { code: 'Argentina', name: '+54' },
  { code: 'Colombia', name: '+57' },
  { code: 'Poland', name: '+48' },
  { code: 'Nigeria', name: '+234' },
  { code: 'Thailand', name: '+66' },
  { code: 'Netherlands', name: '+31' },
  { code: 'Belgium', name: '+32' },
  { code: 'Greece', name: '+30' },
  { code: 'Sweden', name: '+46' },
  { code: 'Denmark', name: '+45' },
  { code: 'Finland', name: '+358' },
  { code: 'Portugal', name: '+351' },
  { code: 'Ireland', name: '+353' },
  { code: 'Austria', name: '+43' },
  { code: 'Switzerland', name: '+41' },
  { code: 'Norway', name: '+47' },
  { code: 'New Zealand', name: '+64' },
  { code: 'Singapore', name: '+65' },
  { code: 'Malaysia', name: '+60' },
  { code: 'Israel', name: '+972' },
  { code: 'Saudi Arabia', name: '+966' },
  { code: 'Turkey', name: '+90' },
  { code: 'South Korea', name: '+82' },
  { code: 'Egypt', name: '+20' }
];

  const selectElement = document.getElementById('country-code');
  
  countryCodes.forEach((country) => {
    const option = document.createElement('option');
    option.value = country.code;
    option.text = country.name;
    selectElement.appendChild(option);
  });


  function showOTPSection() {
    document.getElementById('otp-section').style.visibility = 'visible';
}

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
function sendotp(event) {
  event.preventDefault();
    // Simulate OTP generation and sending
    //alert("OTP sent successfully!");
    // Show OTP input field and Verify button
    //showOTPSection();
    const email = document.getElementById('email').value;
    if (email) {
        fetch('send-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ email: email })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                document.getElementById('otp-section').style.visibility = 'visible';
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
    const otp_1 = document.getElementById('otp_1').value;
    const otp_2 = document.getElementById('otp_2').value;
    const otp_3 = document.getElementById('otp_3').value;
    const otp_4 = document.getElementById('otp_4').value;
    if (email && otp_1 && otp_2 && otp_3 && otp_4) {
        fetch('verify-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ email: email,otp_1: otp_1,otp_2: otp_2,otp_3: otp_3,otp_4: otp_4})
        }).then(response => response.json()).then(data => {
            if (data.success) {
                showModal("Mail verification successful");
                document.getElementById('signup-submit').disabled = false;
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

  /*let inputsAdded = false;
  function myFunction()
  {
    
    if (!inputsAdded) {
    otp='<div class="otp-verification">\
    <input type="text" class="otp-digit" maxlength="1">\
    <input type="text" class="otp-digit" maxlength="1">\
    <input type="text" class="otp-digit" maxlength="1">\
    <input type="text" class="otp-digit" maxlength="1">\
    <button class="verify-otp">Verify</button>\
    </div>'
  }
    
  inputsAdded = true;

const otp_in=document.getElementById('sendOTP')
otp_in.innerHTML+=otp
  }

*/

/*eye icon for signup password field*/
function togglePasswordVisibility() {
  var passwordInput = document.getElementById("signup_password");
  var hideEyeIcon = document.getElementById("hide-eye");
  var revealEyeIcon = document.getElementById("reveal-eye");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      hideEyeIcon.style.display = "none";
      revealEyeIcon.style.display = "inline";
  } else {
      passwordInput.type = "password";
      hideEyeIcon.style.display = "inline";
      revealEyeIcon.style.display = "none";
  }
}

/*eye icon for signin password field*/
function signintogglePasswordVisibility() {
  var passwordInput = document.getElementById("signin_password");
  var hideEyeIcon = document.getElementById("signin_hide-eye");
  var revealEyeIcon = document.getElementById("signin_reveal-eye");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      hideEyeIcon.style.display = "none";
      revealEyeIcon.style.display = "inline";
  } else {
      passwordInput.type = "password";
      hideEyeIcon.style.display = "inline";
      revealEyeIcon.style.display = "none";
  }
}

/*eye icon for confirm password field*/
function confirmPasswordVisibility() {
  var passwordInput = document.getElementById("confirm_password");
  var hideEyeIcon = document.getElementById("confirm_hide-eye");
  var revealEyeIcon = document.getElementById("confirm_reveal-eye");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      hideEyeIcon.style.display = "none";
      revealEyeIcon.style.display = "inline";
  } else {
      passwordInput.type = "password";
      hideEyeIcon.style.display = "inline";
      revealEyeIcon.style.display = "none";
  }
}

function forgot_password(event)
{
  event.preventDefault();
  showModal("Forgot Password");
}