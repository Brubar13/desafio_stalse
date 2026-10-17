
export default function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="alert error" role="alert">
      <strong>Não foi possível carregar os dados.</strong>
      <p>{message}</p>
    </div>
  );
}
