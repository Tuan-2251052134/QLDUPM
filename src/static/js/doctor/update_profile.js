const addDropFileEvent = () => {
  const certificateInputContainers = document.getElementsByClassName(
    "certificateInputContainer",
  );

  const certificationImages =
    document.getElementsByClassName("certificationImage");
  console.log(certificationImages);

  const certificateInputs = document.getElementsByClassName("certificateInput");
  for (let i = 0; i < certificateInputs.length; i++) {
    let certificateInputContainer = certificateInputContainers[i];
    certificateInputContainer.addEventListener("click", () => {
      certificateInputs[i].click();
    });
    certificateInputContainer.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    certificateInputs[i].addEventListener("change", (e) => {
      const file = e.target.files[0];
      const url = URL.createObjectURL(file);
      certificationImages[i].src = url;
    });

    certificateInputContainer.addEventListener("drop", (e) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      const dt = new DataTransfer();
      dt.items.add(file);
      certificateInputs[i].files = dt.files;
      const url = URL.createObjectURL(file);
      certificationImages[i].src = url;
    });
  }
};

const addChangeAvatarEvent = () => {
  const avatarInput = document.getElementById("avatarInput");
  avatarInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    const url = URL.createObjectURL(file);
    const avatar = document.getElementById("avatar");
    avatar.src = url;
  });
};

window.onload = () => {
  addChangeAvatarEvent();
  addDropFileEvent();
};
