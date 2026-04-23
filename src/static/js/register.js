const rolePickHanlder = () => {
  const form = document.getElementById("form");
  const roleInput = document.getElementById("roleInput");

  const doctorOption = document.getElementById("doctorOption");
  const patientOption = document.getElementById("patientOption");

  doctorOption.addEventListener("click", () => {
    doctorOption.classList.add("active");
    patientOption.classList.remove("active");
    roleInput.value = "DOCTOR";
  });
  patientOption.addEventListener("click", () => {
    patientOption.classList.add("active");
    doctorOption.classList.remove("active");
    roleInput.value = "PATIENT";
  });
};

window.onload = () => {
  rolePickHanlder();
};
