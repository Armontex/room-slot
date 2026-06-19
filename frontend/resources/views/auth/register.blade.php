@extends('layouts.app')

@section('content')
    <h1>Регистрация</h1>
    @if ($errors->any())
        <div>
            @foreach ($errors->all() as $error)
                <p>{{ $error }}</p>
            @endforeach
        </div>
    @endif

    <form method="POST" action="{{ route('register') }}">
        @csrf

        <label>
            Почта
            <input type="email" name="email" value="{{ old('email') }}" required>
        </label>
        <label>
            Пароль
            <input type="password" name="password" required>
        </label>

        <label>
            Повторите пароль
            <input type="password" name="password_confirmation" required>
        </label>

        <button type="submit">Зарегистрироваться</button>
    </form>

    <a href="{{ route('login') }}">Уже есть аккаунт?</a>
@endsection
