<?php
/**
 * Canary GPS → «Abono personalizado» de retuertographicdesign.com
 *
 * Los botones de compra de canarygps.com llegan al producto con:
 *   ?importe=42.00&concepto=Canary%20GPS%20–%20Plan%20anual%20(12%20meses)&origen=planes
 *
 * El formulario del producto lo genera WooCommerce Custom Product Addons Pro (WCPA)
 * con JavaScript. Este fragmento espera a que aparezca y rellena:
 *   - el campo numérico del importe («Custom Amount to pay»), con el valor de `importe`;
 *   - el campo de texto de la referencia («Payment reference»), con el valor de `concepto`.
 * WCPA guarda ambos en el carrito y en el pedido como cualquier otro pago.
 * Además guarda `origen` (página de canarygps.com) como dato oculto del pedido.
 *
 * Instalación: plugin «Code Snippets» (tipo PHP, «Ejecutar en todas partes»)
 * o functions.php del tema hijo. Requiere WooCommerce y WCPA.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Campos de WCPA en la versión inglesa del producto. Si la versión en español
// usa otros nombres, el script usa el primer campo numérico y el primer campo
// de texto del formulario.
const CGPS_CAMPO_IMPORTE    = 'number_4024447191';
const CGPS_CAMPO_REFERENCIA = 'text_9286351413';

function cgps_param( $clave ) {
	return isset( $_GET[ $clave ] ) ? sanitize_text_field( wp_unslash( $_GET[ $clave ] ) ) : '';
}

// 1. Rellenar importe y referencia en la ficha del producto.
add_action( 'wp_footer', function () {
	if ( ! function_exists( 'is_product' ) || ! is_product() ) {
		return;
	}
	$importe  = cgps_param( 'importe' );
	$concepto = cgps_param( 'concepto' );
	if ( '' === $importe && '' === $concepto ) {
		return;
	}
	$importe = '' === $importe ? '' : wc_format_decimal( $importe, 2 );
	if ( '' !== $importe && (float) $importe <= 0 ) {
		$importe = '';
	}
	$datos = array(
		'importe'    => $importe,
		'concepto'   => $concepto,
		'campoImp'   => CGPS_CAMPO_IMPORTE,
		'campoRef'   => CGPS_CAMPO_REFERENCIA,
	);
	?>
	<script>
	(function (d) {
		// WCPA usa campos controlados por React: hay que usar el setter nativo
		// y lanzar «input» para que el plugin registre el valor y recalcule el precio.
		function poner(el, valor) {
			if (!el || !valor) return;
			var proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
			Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, valor);
			el.dispatchEvent(new Event('input', { bubbles: true }));
			el.dispatchEvent(new Event('change', { bubbles: true }));
		}
		function buscar(form, nombre, selector) {
			return form.querySelector('[name="' + nombre + '"], #' + nombre) || form.querySelector(selector);
		}
		var intentos = 0;
		var t = setInterval(function () {
			var form = document.querySelector('form.cart .wcpa_form_outer') || document.querySelector('form.cart');
			var imp = form && buscar(form, d.campoImp, 'input[type="number"]:not([name="quantity"])');
			var ref = form && buscar(form, d.campoRef, 'input[type="text"], textarea');
			if ((imp || !d.importe) && (ref || !d.concepto)) {
				clearInterval(t);
				if (imp && d.importe) {
					if (!imp.getAttribute('step')) imp.setAttribute('step', 'any'); // admite céntimos
					poner(imp, d.importe);
				}
				poner(ref, d.concepto);
			} else if (++intentos > 60) {
				clearInterval(t); // 15 s sin formulario: no se toca nada
			}
		}, 250);
	})(<?php echo wp_json_encode( $datos ); ?>);
	</script>
	<?php
} );

// 2. Página de origen como dato oculto del pedido.
add_action( 'woocommerce_before_add_to_cart_button', function () {
	$origen = sanitize_key( cgps_param( 'origen' ) );
	if ( '' !== $origen ) {
		printf( '<input type="hidden" name="cgps_origen" value="%s">', esc_attr( $origen ) );
	}
} );

add_filter( 'woocommerce_add_cart_item_data', function ( $data ) {
	if ( ! empty( $_POST['cgps_origen'] ) ) {
		$data['cgps_origen'] = sanitize_key( wp_unslash( $_POST['cgps_origen'] ) );
	}
	return $data;
} );

add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $cart_item_key, $values ) {
	if ( ! empty( $values['cgps_origen'] ) ) {
		$item->add_meta_data( '_cgps_origen', $values['cgps_origen'] ); // oculto en el pedido
	}
}, 10, 3 );
