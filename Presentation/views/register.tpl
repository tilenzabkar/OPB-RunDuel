% rebase("base.tpl", user=user, success=success, error=error)

<div class="auth-page">
    <div class="auth-card">
        <div class="text-center mb-4">
            <div class="auth-logo">
                <i class="bi bi-person-plus-fill"></i>
            </div>

            <h1 class="auth-title auth-title-sm">Registracija</h1>
            <p class="auth-subtitle">Ustvari nov RunDuel račun</p>
        </div>

        <form method="post">
            <div class="mb-3">
                <label class="form-label">Uporabniško ime</label>
                <input class="form-control form-control-lg" name="uporabnisko_ime" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Geslo</label>
                <input class="form-control form-control-lg" type="password" name="geslo" required>
            </div>

            <button class="btn btn-primary btn-lg w-100" type="submit">
                Registracija
            </button>
        </form>

        <div class="auth-footer">
            Že imaš račun?
            <a href="{{url('login')}}">Prijavi se</a>
        </div>
    </div>
</div>