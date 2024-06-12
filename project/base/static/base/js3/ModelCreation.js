var del=0;

document.getElementById('add-class-button').addEventListener('click', (event) => {
    event.preventDefault();
    const classContainer = document.getElementById('class-container');
    
    //const 
	newClassBox = document.createElement('div');
    newClassBox.classList.add('class-box');
    
    //const 
	classNumber = classContainer.querySelectorAll('.class-box').length + 1;
	if(del != 0)
	{
		classNumber = classContainer.querySelectorAll('.class-box').length + 3;
	}

    newClassBox.dataset.classId = classNumber;

    newClassBox.innerHTML = `
        <div class="class-header">
            <input type="text" name="class${classNumber}" id="class${classNumber}" class="class-name" style="width: 80.888888px; height: 30px;" value="Class ${classNumber}" readonly>
            <button class="edit-button">✏️</button>
            <div class="menu-container">
                <button class="menu-button">⋮</button>
                <div class="dropdown-menu">
                    <button class="delete-class">Delete Class</button>
                    <!-- class="disable-class">Disable Class</button-->
                </div>
            </div>
        </div>
	<hr>
        <div class="class-body">
            <span>Add DataSet's:</span>
            <div class="button-group">
                <!--button class="webcam-button">Webcam</button-->
                <label class="upload-label">
<svg class="sample-source-icon" width="24" height="24" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path fill="#ffff" fill-rule="evenodd" clip-rule="evenodd" d="M11 7.83L8.41 10.41L7 9L12 4L17 9L15.59 10.42L13 7.83V16H11V7.83ZM6 15H4V18C4 19.1 4.9 20 6 20H18C19.1 20 20 19.1 20 18V15H18V18H6V15Z"></path>
                                </svg>
                    Upload
                    <input type="file" name="file${classNumber}" class="upload-input" multiple>
                </label>
            </div>
        </div>
    `;
    document.getElementById('file-list').value=classNumber;
    document.getElementById('class-list').value=classNumber;
    const addClassButton = document.querySelector('.add-class');
    classContainer.insertBefore(newClassBox, addClassButton);

    addEventListeners(newClassBox);
});

function addEventListeners(classBox) {
    
    const editButton = classBox.querySelector('.edit-button');
    const classNameInput = classBox.querySelector('.class-name');
    const menuButton = classBox.querySelector('.menu-button');
    const deleteButton = classBox.querySelector('.delete-class');
    const uploadInput = classBox.querySelector('.upload-input');

    editButton.addEventListener('click', (event) => {
        event.preventDefault();
        classNameInput.removeAttribute('readonly');
        classNameInput.focus();
        classNameInput.addEventListener('blur', () => {
            classNameInput.setAttribute('readonly', true);
        }, { once: true });
    });

    menuButton.addEventListener('click', (event) => {
        event.preventDefault();
        const menuContainer = classBox.querySelector('.menu-container');
        menuContainer.classList.toggle('open');
    });

    deleteButton.addEventListener('click', (event) => {
        event.preventDefault();
        classBox.remove();
	del+=1;

    });

    uploadInput.addEventListener('change', (event) => {
        event.preventDefault();
        const files = event.target.files;
        console.log(`Uploaded ${files.length} files for ${classNameInput.value}`);
    });
}

// Initialize event listeners for existing class boxes
document.querySelectorAll('.class-box').forEach(addEventListeners);


//advance options

document.addEventListener('DOMContentLoaded', function (event) {
    event.preventDefault();
    var coll = document.getElementsByClassName("collapsible");
    event.preventDefault();
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function (event) {
            event.preventDefault();
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }

    document.getElementById('reset-defaults-btn').addEventListener('click', function (event) {
        event.preventDefault();
        document.getElementById('epochs').value = 50;
        document.getElementById('batch-size').value = 16;
        document.getElementById('learning-rate').value = 0.001;
    });
});

