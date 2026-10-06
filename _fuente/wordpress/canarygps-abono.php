<?php
/**
 * Canary GPS → «Abono personalizado» de retuertographicdesign.com
 *
 * Los botones de compra de canarygps.com llegan al producto con:
 *   ?importe=42.00&concepto=Canary%20GPS%20–%20Plan%20anual%20(12%20meses)&origen=planes
 *
 * Este fragmento:
 *   1. Muestra el concepto en la ficha y lo envía con el formulario (campo oculto).
 *   2. Lo guarda en el carrito, lo enseña en carrito y checkout y lo graba en el pedido.
 *   3. Rellena el campo de importe personalizado con el valor de la URL.
 *
 * Instalación: plugin «Code Snippets» (tipo PHP, «Ejecutar en todas partes»)
 * o functions.php del tema hijo. Requiere WooCommerce.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cgps_es() {
	return 0 === strpos( determine_locale(), 'es' );
}

function cgps_etiqueta() {
	return cgps_es() ? 'Concepto' : 'Description';
}

// 1. Concepto visible y campos ocultos en la ficha del producto.
add_action( 'woocommerce_before_add_to_cart_button', function () {
	$concepto = isset( $_GET['concepto'] ) ? sanitize_text_field( wp_unslash( $_GET['concepto'] ) ) : '';
	if ( '' === $concepto ) {
		return;
	}
	$origen = isset( $_GET['origen'] ) ? sanitize_key( wp_unslash( $_GET['origen'] ) ) : '';
	printf( '<p class="cgps-concepto"><strong>%s:</strong> %s</p>', esc_html( cgps_etiqueta() ), esc_html( $concepto ) );
	printf( '<input type="hidden" name="cgps_concepto" value="%s">', esc_attr( $concepto ) );
	printf( '<input type="hidden" name="cgps_origen" value="%s">', esc_attr( $origen ) );
} );

// 2a. Guardar en el carrito (una línea distinta por concepto).
add_filter( 'woocommerce_add_cart_item_data', function ( $data ) {
	if ( empty( $_POST['cgps_concepto'] ) ) {
		return $data;
	}
	$data['cgps_concepto'] = sanitize_text_field( wp_unslash( $_POST['cgps_concepto'] ) );
	$data['cgps_origen']   = isset( $_POST['cgps_origen'] ) ? sanitize_key( wp_unslash( $_POST['cgps_origen'] ) ) : '';
	$data['cgps_clave']    = md5( $data['cgps_concepto'] . microtime() );
	return $data;
} );

// 2b. Mostrarlo en carrito y checkout.
add_filter( 'woocommerce_get_item_data', function ( $items, $cart_item ) {
	if ( ! empty( $cart_item['cgps_concepto'] ) ) {
		$items[] = array(
			'key'   => cgps_etiqueta(),
			'value' => $cart_item['cgps_concepto'],
		);
	}
	return $items;
}, 10, 2 );

// 2c. Grabarlo en el pedido (visible en el pedido y en los correos).
add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $cart_item_key, $values ) {
	if ( empty( $values['cgps_concepto'] ) ) {
		return;
	}
	$item->add_meta_data( cgps_etiqueta(), $values['cgps_concepto'] );
	if ( ! empty( $values['cgps_origen'] ) ) {
		$item->add_meta_data( '_cgps_origen', $values['cgps_origen'] ); // oculto: página de canarygps.com
	}
}, 10, 3 );

// 3. Rellenar el importe personalizado.
add_action( 'wp_footer', function () {
	if ( ! function_exists( 'is_product' ) || ! is_product() || empty( $_GET['importe'] ) ) {
		return;
	}
	$importe = wc_format_decimal( sanitize_text_field( wp_unslash( $_GET['importe'] ) ), 2 );
	if ( '' === $importe || (float) $importe <= 0 ) {
		return;
	}
	$con_coma = str_replace( '.', wc_get_price_decimal_separator(), $importe );
	?>
	<script>
	(function () {
		var form = document.querySelector('form.cart');
		if (!form) return;
		// Selector del campo de importe. Si tu plugin usa otro nombre, añádelo aquí.
		var campo = form.querySelector(
			'input[name="nyp"], input[name*="price"], input[name*="amount"], input[name*="importe"], ' +
			'input[type="number"]:not([name="quantity"])'
		);
		if (!campo) return;
		campo.value = campo.type === 'number' ? <?php echo wp_json_encode( $importe ); ?> : <?php echo wp_json_encode( $con_coma ); ?>;
		campo.dispatchEvent(new Event('input', { bubbles: true }));
		campo.dispatchEvent(new Event('change', { bubbles: true }));
	})();
	</script>
	<?php
} );
