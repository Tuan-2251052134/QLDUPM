const rolePickHanlder = () => {
  const form = document.getElementById("form");
  const roleInput = document.getElementById("roleInput");
  const doctorInfoContainer = document.getElementById("doctorInfoContainer");

  const doctorOption = document.getElementById("doctorOption");
  const patientOption = document.getElementById("patientOption");

  doctorOption.addEventListener("click", () => {
    doctorOption.classList.add("active");
    patientOption.classList.remove("active");
    roleInput.value = "DOCTOR";
    doctorInfoContainer.style.display = "block";
  });
  patientOption.addEventListener("click", () => {
    patientOption.classList.add("active");
    doctorOption.classList.remove("active");
    roleInput.value = "PATIENT";
    doctorInfoContainer.style.display = "none";
  });
};

window.onload = () => {
  rolePickHanlder();
};
