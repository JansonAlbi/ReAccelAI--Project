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

// Function to send OTP (simulated for demo)
function sendotp(event) {
  event.preventDefault();
    // Simulate OTP generation and sending
    //alert("OTP sent successfully!");
    // Show OTP input field and Verify button
    showOTPSection();
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