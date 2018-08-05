
var currentIndex = 0;

function updateQuestion() {
    $('#question').html(reviewItems[currentIndex].question);
}

function checkAnswer() {
    var answer = $('#input-answer').val();
    var correctAnswer = reviewItems[currentIndex].answer;

    if (answer == correctAnswer) {
        alert('CORRECT!');
    } else {
        alert('WRONG!');
    }

    currentIndex += 1;

    if (currentIndex < reviewItems.length) {
        updateQuestion();
        $('#input-answer').val('');
    } else {
    }
}

$('#btn-submit').mouseup(checkAnswer);
$('#input-answer').keyup(function (event) {
    if (event.which == 13) {
        checkAnswer();
    }
});
updateQuestion();