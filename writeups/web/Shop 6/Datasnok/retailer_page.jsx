import { makeRetailer } from "../db";

export default async function retailer(){
  return (
    <form action={makeRetailer}>
      <div className="d-flex align-items-center justify-content-between mt-4 mb-0">
        <button type="submit" className="btn btn-primary">
          Become retailer
        </button>
      </div>
    </form>
  );
}
