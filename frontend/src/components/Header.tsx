import { Link, useNavigate } from "react-router-dom";

import { useAuthStore } from "../store/auth";

export default function Header() {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="border-b border-gray-200 bg-white">
      <nav className="mx-auto flex max-w-4xl items-center justify-between px-8 py-4">
        <Link to="/" className="text-2xl font-bold text-blue-600">
          conduit
        </Link>
        <ul className="flex items-center gap-4 text-sm">
          <li>
            <Link to="/" className="text-gray-700 hover:text-blue-600">
              Home
            </Link>
          </li>
          {user ? (
            <>
              <li>
                <Link to="/editor" className="text-gray-700 hover:text-blue-600">
                  New Article
                </Link>
              </li>
              <li>
                <Link
                  to={`/profile/${user.username}`}
                  className="text-gray-700 hover:text-blue-600"
                >
                  {user.username}
                </Link>
              </li>
              <li>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="text-gray-700 hover:text-blue-600"
                >
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login" className="text-gray-700 hover:text-blue-600">
                  Sign in
                </Link>
              </li>
              <li>
                <Link to="/register" className="text-gray-700 hover:text-blue-600">
                  Sign up
                </Link>
              </li>
            </>
          )}
        </ul>
      </nav>
    </header>
  );
}
