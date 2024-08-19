function toggleAutocomplete(widgetname) {
  span = document.getElementById("autocomplete-" + widgetname);
  if (span.style.display == "none") {
    select = document.getElementById("selectcontainer-" + widgetname);
    let rect = select.getBoundingClientRect();
    span.style.display = "block";
    span.style.width = rect.width + "px";
    input = document.getElementById("search-" + widgetname);
    input.focus();
  } else {
    span.style.display = "none";
  }
}

function setSearchResult(widgetname, el) {
  var opt = document.createElement("option");
  opt.value = el.dataset.value;
  opt.innerHTML = el.innerHTML;
  search = document.getElementById("selectcontainer-" + widgetname);
  search.appendChild(opt);
  search.value = el.dataset.value;
  toggleAutocomplete(widgetname)
}
function parseresults(widgetname, replace=true) {
  ul = document.getElementById("search-results-" + widgetname);
  if (replace) {
    console.log("cleaning up ul");
    ul.innerHTML = "";
  } else {
    document.querySelectorAll('.more').forEach(e => e.remove());
  }
  scratchpad = document.getElementById("scratchpad-" + widgetname);
  response = JSON.parse(scratchpad.innerHTML);
  for (result in response.results) {
    var text = response.results[result].name;
    var id = response.results[result].id;
    var li = document.createElement("li");
    li.dataset.value = id;
    li.innerHTML = text + " " + id;
    li.onclick = function() {
       setSearchResult(widgetname, this);
    };
    ul.appendChild(li);
  }
  if (response.next) {
    console.log(response.next);
    var li = document.createElement("li");
    li.innerHTML = "...more";
    li.setAttribute("class", "more");
    li.setAttribute("hx-get", response.next.replaceAll('&amp;','&'));
    li.setAttribute("hx-trigger", "intersect");
    li.setAttribute("hx-target", "#scratchpad-" + widgetname);
    li.setAttribute("hx-on::after-request", "parseresults('" + widgetname + "', false)");
    li.setAttribute("hx-swap", "innerHTML");
    htmx.process(li);
    ul.appendChild(li);
  }
}

