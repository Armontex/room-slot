@extends('layouts.app')

@section('content')
    <h1>Авторизация</h1>
    @if ($errors->any())
        <div>
            @foreach ($errors->all() as $error)
                <p>{{ $error }}</p>
            @endforeach
        </div>
    @endif

    <form method="POST" action="{{ route('login') }}">
        @csrf

        <label>
            Почта
            <input type="email" name="email" value="{{ old('email') }}" required>
        </label>
        <label>
            Пароль
            <input type="password" name="password" required>
        </label>

        <button type="submit">Войти</button>
    </form>

    <a href="{{ route('register') }}">Регистрация</a>
@endsection
