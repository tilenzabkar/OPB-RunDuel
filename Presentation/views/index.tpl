% rebase("base.tpl", user=user, success=success, error=error)

<h1>RunDuel</h1>

<p>Tekmuj s prijatelji v tekaških izzivih.</p>

% if user:
    <a class="btn btn-primary" href="{{url('dashboard')}}">Dashboard</a>
% else:
    <a class="btn btn-primary" href="{{url('login')}}">Prijava</a>
    <a class="btn btn-success" href="{{url('register')}}">Registracija</a>
% end