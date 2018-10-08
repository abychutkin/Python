<?php
session_start();
function generateToken() {
    $chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    $lenChars = strlen($chars);
    $token = '';
    $length = 8;
    for ($i = 0; $i < $length; $i++) {
        $token .= substr($chars, rand(1, $lenChars)-1, 1);
    }
    return $token;
}

$login = 'admin';
$password = '987654';
$token = generateToken();


if (isset($_POST['login']) && $_POST['login']==$login && isset($_POST['password']) && $_POST['password']==$password && isset($_SESSION['token']) && $_SESSION['token']==$_POST['token']) {
    echo 'You are logged!';
}
else {
    $_SESSION['token']=$token;
    echo '<form method="POST">';
    echo '<input type="text" name="login"><br>';
    echo '<input type="password" name="password"><br>';
    echo '<input type="hidden" value="'.$token.'" name="token"><br>';
    echo '<input type="submit" name="Submit" value="Submit">';
    echo '</form>';
}
?>
