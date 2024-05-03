/*document.getElementById("train-button").addEventListener("click", function() {
  // Training logic here
});

document.getElementById("inference-button").addEventListener("click", function() {
  // Inference logic here
});*/
//let sectionCounter = 3;
function addSection(event)
{
  event.preventDefault();
document.getElementById("new-class-button").addEventListener("click", function() {
  var newUploadSection = document.createElement("div");
  newUploadSection.classList.add("upload-section");

  var newInputFile = document.createElement("input");
  newInputFile.type = "file";
  newInputFile.classList.add("file-upload");
  //newInputFile.accept = ".csv";
  newInputFile.name = "files[]";// + sectionCounter;

  var newLabel = document.createElement("label");
  newLabel.htmlFor = "class-input";
  newLabel.textContent = "New Class:";

  var newInputText = document.createElement("input");
  newInputText.type = "text";
  newInputText.classList.add("class-input");

  var addNewSectionButton = document.getElementById("new-class-button");
  addNewSectionButton.parentNode.insertBefore(newUploadSection, addNewSectionButton);
  newUploadSection.appendChild(newLabel);
  newUploadSection.appendChild(newInputText);
  newUploadSection.appendChild(newInputFile);
  //sectionCounter++; 
});
}