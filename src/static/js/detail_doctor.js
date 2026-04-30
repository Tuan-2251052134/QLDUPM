const onClick = (id) => {
  const cells = document.querySelectorAll(`.cellActive`);
  const titles = document.querySelectorAll(`.cellActive > .cellTitle`);
  const checkboxs = document.querySelectorAll(`.cellActive > .cellCheckbox`);
  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("cellBooked");
    titles[i].innerText = "Đã chọn";
    checkboxs[i].checked = false;
  }

  const cell = document.querySelector(`#${id}`);
  cell.classList.add("cellBooked");
  const title = document.querySelector(`#${id} > .cellTitle`);
  title.innerText = "Đã đặt";
  const checkbox = document.querySelector(`#${id} > .cellCheckbox`);
  checkbox.checked = !checkbox.checked;
};
