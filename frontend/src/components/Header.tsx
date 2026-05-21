import { Link } from "react-router-dom";

export default function Header() {
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
          <li>
            <Link to="/editor" className="text-gray-700 hover:text-blue-600">
              New Article
            </Link>
          </li>
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
        </ul>
      </nav>
    </header>
  );
}
