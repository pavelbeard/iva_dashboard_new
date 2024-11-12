import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { Mutex } from "async-mutex";
import { setToken, setUser, signOut } from "../../../features/store/authSlice";

const baseUrl = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL + "/api"
  : "/api";

const mutex = new Mutex();
const baseQuery = fetchBaseQuery({
  baseUrl,
  credentials: "include",
  prepareHeaders: (headers) => {
    headers.set("Content-Type", "application/json");
    return headers;
  },
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
  await mutex.waitForUnlock();
  let result = await baseQuery(args, api, extraOptions);

  if (result?.error?.status === 403 || result?.error?.status === 401) {
    if (mutex.isLocked()) {
      const release = await mutex.acquire();
      try {
        const token = api.getState().auth.token;
        const refreshResult = await baseQuery(
          {
            url: "/stuff/token/refresh/",
            method: "POST",
            body: JSON.stringify({ access: token }),
          },
          api,
          extraOptions,
        );

        if (refreshResult?.data?.access) {
          const user = api.getState().auth.user;
          api.dispatch(setToken({ ...refreshResult.access }));
          api.dispatch(setUser({ user }));
          result = await baseQuery(args, api, extraOptions);
        } else {
          api.dispatch(signOut());
        }
      } finally {
        release();
      }
    } else {
      await mutex.waitForUnlock();
      result = await baseQuery(args, api, extraOptions);
    }
  }
  return result;
};

export const apiSlice = createApi({
  baseQuery: baseQueryWithReauth,
  endpoints: (builder) => ({}),
});
