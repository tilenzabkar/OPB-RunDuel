% rebase("base.tpl", user=user, success=success, error=error)

<h1>RunDuel</h1>

<p>Tekmuj s prijatelji v tekaških izzivih.</p>

% if user:
    <a class="btn btn-primary" href="/dashboard">Dashboard</a>
% else:
    <a class="btn btn-primary" href="/login">Prijava</a>
    <a class="btn btn-success" href="/register">Registracija</a>
% end