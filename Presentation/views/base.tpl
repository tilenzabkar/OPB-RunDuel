<!doctype html>
<html lang="sl">
<head>
    <meta charset="utf-8">
    <title>RunDuel</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" href="/static/style.css">
</head>

<body class="bg-light">

<nav class="navbar navbar-expand navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">RunDuel</a>

        <div class="navbar-nav">
            % if user:
                <a class="nav-link" href="/dashboard">Dashboard</a>
                <a class="nav-link" href="/runs">Teki</a>
                <a class="nav-link" href="/challenges">Izzivi</a>
                <a class="nav-link" href="/users">Uporabniki</a>
                <a class="nav-link" href="/logout">Odjava</a>
            % else:
                <a class="nav-link" href="/login">Prijava</a>
                <a class="nav-link" href="/register">Registracija</a>
            % end
        </div>
    </div>
</nav>

<div class="container">

    % if success:
        <div class="alert alert-success">
            {{success}}
        </div>
    % end

    % if error:
        <div class="alert alert-danger">
            {{error}}
        </div>
    % end

    {{!base}}

</div>

</body>
</html>
