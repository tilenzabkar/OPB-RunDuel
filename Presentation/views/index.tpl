% rebase("base.tpl", user=user, success=success, error=error)

<div class="auth-page">
    <div class="auth-card">
        <div class="text-center mb-4">
            <div class="auth-logo">
                <i class="bi bi-lightning-charge-fill"></i>
            </div>

            <h1 class="auth-title">RunDuel</h1>
            <p class="auth-subtitle">Prijavi se v svoj račun</p>
        </div>

        % if user:
            <a class="btn btn-primary btn-lg w-100" href="{{url('dashboard')}}">
                Pojdi na dashboard
            </a>
        % else:
            <form method="post" action="{{url('login')}}">
                <div class="mb-3">
                    <label class="form-label">Uporabniško ime</label>
                    <input class="form-control form-control-lg" name="uporabnisko_ime" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Geslo</label>
                    <input class="form-control form-control-lg" type="password" name="geslo" required>
                </div>

                <button class="btn btn-primary btn-lg w-100" type="submit">
                    Prijava
                </button>
            </form>

            <div class="auth-footer">
                Nimaš še računa?
                <a href="{{url('register')}}">Registriraj se</a>
            </div>
        % end
    </div>
</div>