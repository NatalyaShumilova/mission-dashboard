/// <reference types="react-scripts" />

declare namespace NodeJS {
  interface ProcessEnv {
    readonly REACT_APP_MAPBOX_TOKEN: string;
    readonly REACT_APP_API_BASE_URL: string;
  }
}
