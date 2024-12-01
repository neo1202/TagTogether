import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();

  return (
    <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div className="flex flex-wrap">
        <div className="w-full md:w-1/2 md:ml-[25%] px-4">
          <h1 className="mt-6">Oops!</h1>
          <p>Sorry, an unexpected error has occurred.</p>
          <p>
            <em>{error.statusText || error.message}</em>
          </p>
        </div>
      </div>
    </div>
  );
}
