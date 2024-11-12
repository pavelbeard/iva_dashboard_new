import { apiSlice } from "./apiSlice";

const apiWithTags = apiSlice.enhanceEndpoints({

});

export const authApiSlice = apiWithTags.injectEndpoints({

})