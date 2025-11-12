import { html } from "../../_npm/htl@0.3.1/72f4716c.js";

export function autoSelect(options, format = (d) => d, initialValue = null) {
  const formattedOptions = options.map(format);
  const listId = "autocomplete-" + Math.random().toString(36).substr(2, 9);
  const dropdownId = "dropdown-" + Math.random().toString(36).substr(2, 9);
  const initialDisplay = initialValue ? format(initialValue) : "";

  const form = html`<form class="autocomplete-form">
    <div class="autocomplete-wrapper">
      <input 
        type="text" 
        name="input" 
        class="autocomplete-input" 
        id="${listId}"
        value="${initialDisplay}"
        autocomplete="off"
        placeholder="">
      <div class="autocomplete-dropdown" id="${dropdownId}"></div>
    </div>
  </form>`;

  const input = form.querySelector("input");
  const dropdown = form.querySelector(".autocomplete-dropdown");
  let selectedIndex = -1;
  let currentFilteredOptions = [];

  form.value = initialValue || null;
  form.onsubmit = (e) => e.preventDefault();

  function filterOptions(query) {
    if (!query) return formattedOptions;
    return formattedOptions.filter((opt) =>
      opt.toLowerCase().includes(query.toLowerCase())
    );
  }

  function showDropdown(items) {
    currentFilteredOptions = items;

    if (items.length === 0) {
      dropdown.innerHTML = "";
      const option = html`<div class="autocomplete-option no-results">no encuentro esa ciudad 🤷</div>`;
      dropdown.appendChild(option);
    } else {
      dropdown.innerHTML = "";
      items.forEach((item, index) => {
        const option = html`<div class="autocomplete-option" data-index="${index}">${item}</div>`;

        option.addEventListener("click", () => {
          input.value = item;
          hideDropdown();
          updateFormValue(item);
        });

        dropdown.appendChild(option);
      });
    }

    dropdown.classList.add("show");
    selectedIndex = -1;
  }

  function hideDropdown() {
    dropdown.classList.remove("show");
    selectedIndex = -1;
  }

  function updateSelection(direction) {
    const optionElements = dropdown.querySelectorAll(
      ".autocomplete-option:not(.no-results)"
    );
    if (optionElements.length === 0) return;

    optionElements.forEach((opt) => opt.classList.remove("selected"));

    if (direction === "down") {
      selectedIndex = (selectedIndex + 1) % optionElements.length;
    } else if (direction === "up") {
      selectedIndex =
        selectedIndex <= 0 ? optionElements.length - 1 : selectedIndex - 1;
    }

    optionElements[selectedIndex].classList.add("selected");
    optionElements[selectedIndex].scrollIntoView({ block: "nearest" });
  }

  function updateFormValue(displayValue) {
    const matchedObject = options.find((obj) => format(obj) === displayValue);
    if (matchedObject) {
      form.value = matchedObject;
      form.dispatchEvent(new CustomEvent("input", { bubbles: true }));
    }
  }

  input.addEventListener("input", (e) => {
    e.stopPropagation();
    const filtered = filterOptions(e.target.value);
    showDropdown(filtered);
    updateFormValue(e.target.value);
  });

  input.addEventListener("focus", () => {
    const filtered = filterOptions(input.value);
    showDropdown(filtered);
  });

  input.addEventListener("keydown", (e) => {
    if (!dropdown.classList.contains("show")) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      updateSelection("down");
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      updateSelection("up");
    } else if (e.key === "Enter") {
      e.preventDefault();
      const selected = dropdown.querySelector(".autocomplete-option.selected");
      if (selected && !selected.classList.contains("no-results")) {
        input.value = selected.textContent;
        hideDropdown();
        updateFormValue(selected.textContent);
      }
    } else if (e.key === "Escape") {
      hideDropdown();
    }
  });

  document.addEventListener("click", (e) => {
    if (
      !e.target.closest(`#${listId}`) &&
      !e.target.closest(`#${dropdownId}`)
    ) {
      hideDropdown();
    }
  });

  return form;
}