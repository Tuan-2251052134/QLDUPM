const rolePickHanlder = () => {
  const form = document.getElementById("form");
  const roleInput = document.getElementById("roleInput");
  const doctorInfoContainer = document.getElementById("doctorInfoContainer");

  const doctorOption = document.getElementById("doctorOption");
  const patientOption = document.getElementById("patientOption");
  const certifcateCard = document.getElementById("certifcateCard");

  doctorOption.addEventListener("click", () => {
    doctorOption.classList.add("active");
    patientOption.classList.remove("active");
    roleInput.value = "DOCTOR";
    doctorInfoContainer.style.display = "block";
    certifcateCard.style.display = "flex";
  });
  patientOption.addEventListener("click", () => {
    patientOption.classList.add("active");
    doctorOption.classList.remove("active");
    roleInput.value = "PATIENT";
    doctorInfoContainer.style.display = "none";
    certifcateCard.style.display = "none";
  });
};

const addDropFileEvent = () => {
  const certificateInputContainer = document.getElementById(
    "certificateInputContainer",
  );

  const certificateInput = document.getElementById("certificateInput");
  certificateInputContainer.addEventListener("dragover", (e) => {
    e.preventDefault(); // bắt buộc
  });
  certificateInputContainer.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    const dt = new DataTransfer();
    dt.items.add(file);
    certificateInput.files = dt.files;
  });
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
  rolePickHanlder();
  addDropFileEvent();
  addChangeAvatarEvent();
};
