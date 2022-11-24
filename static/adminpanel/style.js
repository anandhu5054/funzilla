function expand() {
    var element = document.getElementById("sidenav");
    element.classList.remove("is-collapsed");
  }
  
  function collapse() {
    var element = document.getElementById("sidenav");
    element.classList.add("is-collapsed");
  }
  
  function toggle() {
    var element = document.getElementById("sidenav");
    element.classList.toggle("is-collapsed");
  }