from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

# Configurações do Instagram
CLIENT_ID = "1192672039076047"
CLIENT_SECRET = "13988311217058edd577fc254e8244ae"
REDIRECT_URI = "https://get-api-insta-followers.onrender.com/callback"


@app.route('/')
def home():
    """Redireciona diretamente para o autenticador do Instagram"""
    auth_url = (
        f"https://www.instagram.com/oauth/authorize?"
        f"enable_fb_login=0&force_authentication=1"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish"
    )
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Rota para processar o código retornado pelo Instagram"""
    code = request.args.get('code')
    if not code:
        return """
            <script>
                window.opener.alert('Nenhum código foi retornado pelo Instagram.');
                window.close();
            </script>
        """

    # Trocar o código pelo token de acesso
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return f"""
            <script>
                window.opener.alert('Erro ao obter o token de acesso: {response.text}');
                window.close();
            </script>
        """

    body = response.json()
    access_token = body.get("access_token")
    user_id = body.get("user_id")

    # Obter informações do perfil
    profile_url = f"https://graph.instagram.com/v21.0/me?fields=id,username,account_type,media_count,followers_count&access_token={access_token}"
    profile_response = requests.get(profile_url)

    if profile_response.status_code != 200:
        return f"""
            <script>
                window.opener.alert('Erro ao obter informações do perfil: {profile_response.text}');
                window.close();
            </script>
        """

    profile_data = profile_response.json()
    followers = profile_data.get("followers_count", 0)

    # Geração do script para comunicar à página original
    if followers > 5000000:
        return f"""
            <script>
                window.opener.location.href = "https://exercitodeinfluencia.com.br/5mm/";
                window.close();
            </script>
        """
    elif followers > 1000000:
        return f"""
            <script>
                window.opener.location.href = "https://exercitodeinfluencia.com.br/1mm-a-5mm/";
                window.close();
            </script>
        """
    elif followers > 500000:
        return f"""
            <script>
                window.opener.location.href = "https://exercitodeinfluencia.com.br/500k-a-1mm/";
                window.close();
            </script>
        """
    elif followers > 100000:
        return f"""
            <script>
                window.opener.location.href = "https://exercitodeinfluencia.com.br/100k-a-500k/";
                window.close();
            </script>
        """
    else:
        return """
            <script>
                window.opener.document.getElementById('form-container').style.display = 'block';
                window.close();
            </script>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
