document.addEventListener("DOMContentLoaded", function () {
  function toggleColumnVisibility(columnClass, isVisible) {
    var columns = document.getElementsByClassName(columnClass);
    for (var i = 0; i < columns.length; i++) {
      columns[i].style.display = isVisible ? "" : "none";
    }
  }

  var checkboxes = document.querySelectorAll(
    '.fracas-custom-dropdown-menu input[type="checkbox"]'
  );
  checkboxes.forEach(function (checkbox) {
    var columnClass = checkbox.getAttribute("data-field");
    toggleColumnVisibility(columnClass, checkbox.checked);
  });

  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      var columnClass = checkbox.getAttribute("data-field");
      toggleColumnVisibility(columnClass, checkbox.checked);
    });
  });
});
