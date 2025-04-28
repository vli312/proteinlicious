$(document).ready(function() {
  // Event handler for go button in nav bar
  checkQueryString();

  // Interaction 1: DOM traversal. Fades the comment-box (parent) in AlternativeChickenCurry.html when the comment bar or button is clicked
  $('#alt-comment-bottom').on("click", function(event) {
    $(this).parent().fadeTo(500, 0.5);
    var logInMessage = $('<p class="log-in-message">You must log in to leave comments</p>');
    $(logInMessage).appendTo($(this).parent().parent()).fadeOut(500, function(){
      $(this).remove();
    });
  });
  // Stops the button from refreshing the page
  $('input#locked').on("click", function(event) {
    event.preventDefault();
  });

  // Interaction 2: Event Delegation.
  // Adds a pop up alert describing what the protein in the side bar is in list.html
  $("ul#side-tab a").on("mouseover", function(event) {
    let message = "";
    if ($(this).text() === 'Vegetarian' || $(this).text() === 'Gluten Free' || $(this).text() === 'Nut Free') {
      message = "This features recipes that are " + $(this).text() + " friendly.";
    } else {
      message = "This features recipes using " + $(this).text() + " as the primary protein source.";
    }
    $("#alert").text(message).show();
  }).on("mouseleave", function(event) {
    $("#alert").hide();
  });

  // Adds a highlight when hovering over a row in the grid in list.html
  $("table#table").on("mouseover", "tbody tr", function(event){
    $(this).css("background-color", "lightblue"); // Highlight the row
  }).on("mouseleave", "tbody tr", function(event) {
    $(this).css("background-color", ""); // Remove the highlight
  });

  adminDeletePopUp();
  adminChangeUserPopUp()

  addIngredientsRow();
  minusIngredientsRow();

  addNutritionRow();
  minusNutritionRow();

  addInstructionsRow();
  minusInstructionsRow();

  addSort();
  ajax();
});

// function for the search bar requirement 
function checkQueryString(){
  var queryString = window.location.search;
  var urlParams = new URLSearchParams(queryString);
  if (urlParams.has('search-bar')){
    var keyword = urlParams.get('search-bar');
    if(keyword == 'Chicken' || keyword == 'chicken'){
      var ChickenHeading = $('<h3 class="search-result">Chicken</h3>');
      var ChickenColectionLink = $('<a class="chickenLink" href="list.html">Chicken Collection</a>');
      var ChickenRecipe1 = $('<a class="chickenLink" href="chickenCurry.html">Chicken Curry Recipe</a>');
      var ChickenRecipe2 = $('<a class="chickenLink" href="#">Chicken Pad Thai Recipe</a>');
      var ChickenRecipe3 = $('<a class="chickenLink" href="#">Chicken Pad See Ew Recipe</a>');
      var ChickenRecipe4 = $('<a class="chickenLink" href="#">Chicken Tortas Recipe</a>');
      var ChickenRecipe5 = $('<a class="chickenLink" href="#">Chicken Dip Recipe</a>');
      var ChickenRecipe6 = $('<a class="chickenLink" href="#">Chicken Alfredo Recipe</a>');
      $('#content').append(ChickenHeading);
      $('#content').append(ChickenColectionLink);
      $('#content').append(ChickenRecipe1);
      $('#content').append(ChickenRecipe2);
      $('#content').append(ChickenRecipe3);
      $('#content').append(ChickenRecipe4);
      $('#content').append(ChickenRecipe5);
      $('#content').append(ChickenRecipe6);
    } else {
      window.alert("There are no search results. Please search Chicken or chicken");
    }
  }
}

// Project 4: presents a pop-up for deleting a recipe from the listview
function adminDeletePopUp() {
  $('button#delete-user').on("click", function(event) {
    //event.preventDefault();
    confirm("Do you wish to delete this entry?");
  });
}

function adminChangeUserPopUp() {
  $('button#change-user').on("click", function(event) {
    //event.preventDefault();
    confirm("Do you wish to update this user's role?");
  });
}

// upload and edit add row for ingredients
function addIngredientsRow() {
  $('button#ingredients-button-add').on("click", function(event) {
    event.preventDefault();
    var newInput = $('<label><input class="input-box" name="ingredients" placeholder="Insert Text Here" required></label>');
    newInput.insertBefore($('#upload-ing'));
  });
}

// upload and edit minus row for ingredients
function minusIngredientsRow() {
  $('button#ingredients-button-minus').on("click", function(event) {
    event.preventDefault();
    if ($('#add-ingredients').children().length > 2){
        $('#upload-ing').prev().remove();
    } else {
        alert("You must have one ingredient!");
    }
  });
}

// upload and edit add row for nutrition
function addNutritionRow() {
  $('button#nutrition-button-add').on("click", function(event) {
    event.preventDefault();
    var newInput = $('<tr class="newtr"><td><input type="text" name="nutritionName" placeholder="Ingredient"></td><td><input type="number" name="nutritionCal" placeholder="0"></td><td><input type="number" name="nutritionCarb" placeholder="0"></td><td><input type="number" name="nutritionFat" placeholder="0"></td><td><input type="number" name="nutritionProtein" placeholder="0"></td></tr>');
    $("#nutrition-table:last-child").append(newInput);
  });
}

// upload and edit minus row for nutrition
function minusNutritionRow() {
  $('button#nutrition-button-minus').on("click", function(event) {
    event.preventDefault();
    if ($("#nutrition-table tr").length > 2){
        $("#nutrition-table tr:last-child").remove();
    } else {
        alert("You must have one ingredient nutrition!");
    }
  });
}

// upload and edit add row for instructions
function addInstructionsRow() {
  $('button#instructions-button-add').on("click", function(event) {
    event.preventDefault();
    var newInput = $('<label><input class="input-box" name="instructions" placeholder="Step X: Insert Text Here"></label>');
    newInput.insertBefore($('#upload-ins'));
  });
}

// upload and edit minus row for instructions
function minusInstructionsRow() {
  $('button#instructions-button-minus').on("click", function(event) {
    event.preventDefault();
    if ($('#ins-input').children().length > 6){
        $('#upload-ins').prev().remove();
    } else {
        alert("You must have one instruction!");
    }
  });
}

// list view table sort
function addSort(){
  $("table#table th").on("click", function() {
        var columnIndex = $(this).index();
        var table = $("table#table").get(0);
        var tbody = $(table).find("tbody");
        var isAscending = $(this).hasClass("asc");
        $("table#table th").removeClass("asc desc");
        $(this).addClass(isAscending ? "desc" : "asc");
        var rows = tbody.find("tr").get();
        rows.sort(function(a, b) {
            var A = $(a).children("td").eq(columnIndex).text().toUpperCase();
            var B = $(b).children("td").eq(columnIndex).text().toUpperCase();
            if ($.isNumeric(A) && $.isNumeric(B)) {
                A = parseFloat(A);
                B = parseFloat(B);
            }
            if (isAscending) {
                return (A < B) ? -1 : (A > B) ? 1 : 0;
            } else {
                return (A > B) ? -1 : (A < B) ? 1 : 0;
            }
        });
        $.each(rows, function(index, row) {
            tbody.append(row);
        });
    });
}

// ajax function for project 5 requirement that retrieves data and modifies data for the comments attribute and box for the recipe_detail
function ajax(){
    $('button#comment-button').on("click", function(event) {
        var story_id = $(this).attr('data-story-id');
        var ajax_url = $(this).attr('data-ajax-url');
        var commentText = $('#comment-text').val();
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                story_id: story_id,
                comment_text: commentText,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this,
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
             if(json.success == 'success') {
                var logInMessage = $('<p class="log-in-message">Successfully added comment</p>');
                $(logInMessage).appendTo($(this).parent().parent().parent()).fadeOut(700, function(){
                  $(this).remove();
                });
                $('#comments-list').empty(); // Clear the existing comments
                $.each(json.comments, function(index, comment) {
                    $('#comments-list').append(`
                        <li>
                            <img src='/static/img/personIcon.png'  alt='PersonIcon'>
                            <p><strong>${comment.name}</strong> - ${comment.date}:</p>
                            <p>${comment.text}</p>
                        </li>
                    `);
                });
                $('#comments-section h3').text(`Comments [${json.comments.length}]`);
                $('#comment-text').val('');
             } else {
                alert("Error: " + json.error);
             }
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
        alert( "Sorry, there was a problem!" );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });
}

// required CSRF cookie property for AJAX to modifiy
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');