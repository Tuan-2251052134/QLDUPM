const onClick = (id) => {
  const cell = document.querySelector(`#${id}`);
  cell.classList.toggle("cellActive");
  const title = document.querySelector(`#${id} > #title`);
  title.classList.toggle("titleShow");
  const checkbox = document.querySelector(`#${id} > #cellCheckbox`);
  checkbox.checked = !checkbox.checked;
};
