var del=0;

document.getElementById('add-class-button').addEventListener('click', () => {
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
            <input type="text" class="class-name" style="width: 80.888888px; height: 30px;" value="Class ${classNumber}" readonly>
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
                    <input type="file" class="upload-input">
                </label>
            </div>
        </div>
    `;

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

    editButton.addEventListener('click', () => {
        classNameInput.removeAttribute('readonly');
        classNameInput.focus();
        classNameInput.addEventListener('blur', () => {
            classNameInput.setAttribute('readonly', true);
        }, { once: true });
    });

    menuButton.addEventListener('click', () => {
        const menuContainer = classBox.querySelector('.menu-container');
        menuContainer.classList.toggle('open');
    });

    deleteButton.addEventListener('click', () => {
        classBox.remove();
	del+=1;

    });

    uploadInput.addEventListener('change', (event) => {
        const files = event.target.files;
        console.log(`Uploaded ${files.length} files for ${classNameInput.value}`);
    });
}

// Initialize event listeners for existing class boxes
document.querySelectorAll('.class-box').forEach(addEventListeners);
