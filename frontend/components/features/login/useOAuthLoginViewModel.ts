import { useResolve } from "ts-injecty";
import { onMounted, ref } from "vue-demi";
import {
  OAuthProvider,
  ProviderType,
} from "~/v1/domain/entities/oauth/OAuthProvider";
import { OAuthLoginUseCase } from "~/v1/domain/usecases/oauth-login-use-case";

export const useOAuthLoginViewModel = () => {
  const oauthLogin = useResolve(OAuthLoginUseCase);
  const providers = ref<OAuthProvider[]>([]);

  onMounted(() => {
    loadProviders();
  });

  const loadProviders = async () => {
    try {
      providers.value = await oauthLogin.getProviders();
    } catch (error) {}
  };

  const authorize = (provider: ProviderType) => {
    window.location.href =
      "https://frascuchon-oauth2-app-test.hf.space/oauth2/huggingface/authorize";
  };

  return {
    providers,
    authorize,
  };
};
